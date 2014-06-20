"""
File: requesthandler.py 
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/6/18
"""
"""
These functions provide request handling, leaving the views receive requests and sending real HTTP CEES responses.
"""
import ceesvalidator as cv
import ceesdbwrapper as cdbw
import constants as c
import logmessages as lm
import pushnotification as pn
from ceesloggers import getCeesAppLogger

applogger = getCeesAppLogger()

####################
# Common functions #
####################

def getToken(request):
  """
  Checks the Authentication header containing the token.
  """
  try:
    tokenId = request.META[c.AUTHENTICATION] #request.META[c.AUTHENTICATION]
  except KeyError as re:
    applogger.exception(lm.MISSING_TOKEN + '\n' + str(re))
    return (c.UNAUTHORIZED, '')
  token = cdbw.getToken(tokenId)
  if token == c.OBJECT_NOT_FOUND:
    applogger.warning(lm.TOKEN_NOT_FOUND)
    return (c.UNAUTHORIZED, '')
  elif token == c.DB_ERROR:
    applogger.error(lm.DB_ERROR)
    return (c.INTERNAL_SERVER_ERROR, '')
  return (c.OK, token)

#############################################
# Functions related to login: login, logout #
#############################################

def login(request):
  """
  Login shop assistants. If email and password matches returns a token.
  """
  data = request.DATA # Parsing request. If it is malformed, Django will return HTTP 400 automatically.
  validation_result = cv.CeesValidator().validate(data, c.LOGIN) # Validating request against schema.
  if validation_result == c.VALID_SUCC: # Validation successful. Extracting data.
    email = data.get(c.EMAIL, False)
    password = data.get(c.PASSWORD, False)
    macAddress = data.get(c.MAC_ADDRESS, False)
    auth = cdbw.checkLoginCredentials(email, password, macAddress) # Checking credentials.
    if auth == c.OBJECT_NOT_FOUND: # Credentials not found. Returns HTTP 401.
      applogger.warning(lm.CREDENTIALS_NOT_FOUND)
      return (c.UNAUTHORIZED, '')
    elif auth == c.DB_ERROR: # Could not persist token. Returns HTTP 500.
      applogger(lm.DB_ERROR)
      return (c.INTERNAL_SERVER_ERROR, '')
    applogger.info(lm.LOGGED_IN + email)
    return (c.CREATED, auth) # Ok. Returns HTTP 201.
  elif validation_result == c.IOERR: # IOError. Returns HTTP 500.
    applogger.error(lm.SCHEMA_NOT_FOUND)
    return (c.INTERNAL_SERVER_ERROR, '')
  applogger.error(lm.VALIDATION_ERROR)
  return (c.BAD_REQUEST, '') # Validation Error. Returns HTTP 400.


def logout(request):
  """
  Deletes the token from database causing the log-out.
  """
  try:
    if cdbw.deleteToken(request.META[c.AUTHENTICATION]) == c.SUCC_QUERY: 
      return c.OK # Ok. Returns HTTP 200.
    else:
      applogger.error(lm.DB_ERROR)
      return c.INTERNAL_SERVER_ERROR # Database error. Returns HTTP 500.
  except KeyError as re: # If no Authentication header found, returns HTTP 401.
    applogger(lm.MISSING_TOKEN)
    return c.UNAUTHORIZED


#######################################################################
# Functions related to check-in process: getStores, checkin, checkout #
#######################################################################

def getStores(request):
  """
  Given the token obtained during the login retrieves the sotores available for the linked shop assistant.
  """
  (status, token) = getToken(request) # Check the token in the Authentication header.
  if status != c.OK:
    return (status, '')
  tokenId = token.id  # If the token is present and valid, get the linked shop assistant.
  sa = cdbw.getShopAssistant(tokenId)
  if sa == c.DB_ERROR: 
    applogger(lm.DB_ERROR)
    return Response(c.INTERNAL_SERVER_ERROR, '')
  customer = cdbw.getCustomer(sa.id)
  if customer == c.DB_ERROR: 
    applogger(lm.DB_ERROR)
    return Response(c.INTERNAL_SERVER_ERROR, '')
  stores = cdbw.getStores(customer.id) # If no error, get the customer linked to a shop assistant.
  if stores == c.OBJECT_NOT_FOUND: 
    applogger.warning(lm.STORE_NOT_FOUND)
    return Response(c.NOT_FOUND, '')
  elif stores == c.DB_ERROR:
    applogger.error(lm.DB_ERROR)
    return Response(c.INTERNAL_SERVER_ERROR, '')
  return Response(c.OK, stores) # If no error, return the store list linked to a customer.

def checkin(request):
  """
  Given a store (city, address), this function will persist the shop assistant and the store in database.
  """
  (status, token) = getToken(request) # Check the token in the Authentication header.
  if status != c.OK:
    return status
  tokenId = token.id  # If the token is present and valid, get the linked shop assistant.
  sa = cdbw.getShopAssistant(tokenId)
  device = cdbw.getDevice(tokenId)
  if sa == c.DB_ERROR or device == c.DB_ERROR: # If there is no shop assistant or device linked to the token it's a database error.
    return c.INTERNAL_SERVER_ERROR
  regId = cdbw.getRegistrationId(device)
  if regId == c.OBJECT_NOT_FOUND:
    return c.NOT_FOUND
  elif regId == c.DB_ERROR:
    return c.INTERNAL_SERVER_ERROR
  data = request.DATA # Parsing request. If it is malformed, Django will return HTTP 400 automatically.
  validationResult = cv.CeesValidator().validate(data, c.CHECKIN) # Validating request against schema.
  if validationResult == c.VALID_SUCC: # Validation successful. Extracting data.
    city = data.get(c.CITY)
    address = data.get(c.ADDRESS)
    store = cdbw.getStore(city, address)
    if store == c.OBJECT_NOT_FOUND: # Very rare. This is checking that the store was deleted after the login but before the checkin.
      return c.NOT_FOUND
    elif store == c.DB_ERROR:
      return c.INTERNAL_SERVER_ERROR
    else:
      if cdbw.checkIn(token, regId, store) != c.SUCC_QUERY:
        return c.INTERNAL_SERVER_ERROR
      return c.CREATED # Checkin persisted. HTTP 201.
  return c.BAD_REQUEST # Validation Error. Returns HTTP 400.

def checkout(request):
  """
  This function removes the entry in check_ins for the shop assistant linked to the token in the request.
  """
  (status, token) = getToken(request) # Check the token in the Authentication header.
  if status != c.OK:
    return status
  if cdbw.checkOut(token) == c.SUCC_QUERY: # Deleted entry in check-ins table.
    return c.OK
  return c.INTERNAL_SERVER_ERROR

##################################################################
# Function related to client arrivals: newArrival, getClientInfo #
##################################################################

def newArrival(request):
  """
  Stores a new arrival and send notification to shop assistants who have checked-in the store linked to the given request.
  """
  data = request.DATA # Parsing request. If it is malformed, Django will return HTTP 400 automatically.
  validationResult = cv.CeesValidator().validate(data, c.DETECT) # Validating request against schema.
  if validationResult == c.VALID_SUCC: # Validation successful. Extracting data.
    customerId = data.get(c.CUSTOMERID, False)
    storeId = data.get(c.STOREID, False)
    rfid = data.get(c.RFID, False)
    client = cdbw.getClientFromRFID(rfid)
    if client == c.OBJECT_NOT_FOUND:
      applogger.warning(lm.RFID_NOT_FOUND)
      return c.NOT_FOUND
    elif client == c.DB_ERROR:
      applogger.error(lm.DB_ERROR)
      return c.INTERNAL_SERVER_ERROR
    if client.customer.id != customerId: # Client who enter in a store which is owned by a different customer.
      applogger.error(lm.CLIENT_NOT_ALLOWED)
      return c.FORBIDDEN
    store = cdbw.getStoreFromId(storeId)
    if store == c.OBJECT_NOT_FOUND:
      applogger.warning(lm.STORE_NOT_FOUND)
      return c.NOT_FOUND
    elif store == c.DB_ERROR:
      applogger.error(lm.DB_ERROR)
      return c.INTERNAL_SERVER_ERROR
    if cdbw.saveArrival(client, store) == c.DB_ERROR: # Everything OK. Save arrival.
      applogger.error(lm.DB_ERROR)
      return c.INTERNAL_SERVER_ERROR
    registrationIds = cdbw.getRegistrationIds(store)
    if registrationIds != c.OBJECT_NOT_FOUND and registrationIds != c.DB_ERROR and registrationIds != []:
      applogger.info(lm.SENDING_NOTIFICATION)
      pn.sendNotification(registrationIds, client)
    return c.CREATED
  return c.BAD_REQUEST # Validation Error. Returns HTTP 400.


