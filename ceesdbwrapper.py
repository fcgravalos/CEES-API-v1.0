"""
File: ceesdbwrapper.py
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/05
"""
"""
This script wraps queries to data model (CEES database).
This keeps the view handling requests and responses.
"""
import constants as c
###################################################################
# set-up to run a model query from ceesdbwrapper. 
###################################################################
from os import path as os_path, environ
from sys import path as sys_path
sys_path.append(os_path.abspath(os_path.join(os_path.dirname(__file__), os_path.pardir)))
environ.setdefault(c.DJANGO_SETTINGS, c.CEES_SETTINGS)
####################################################################
import uuid
from datetime import datetime
from django.db import Error
from cees.models import ShopAssistants, Tokens, Devices, Stores, SaRegistrations, CheckIns, Clients, Customers, RfidCards, ClientArrivals
from ceesloggers import getDbLogger 


dblogger = getDbLogger()
DB_ERRORS = { 0 : c.SUCC_QUERY, 1 : c.OBJECT_NOT_FOUND, 2 : c.DB_ERROR}

#################
# Authorization #
#################

def getToken(tokenId):
  """
  This function checks that the token given in Authorization Header is present in CEES database.
  Returns:
    - A token if the shop assistant and device are registered in CEES database.
    - OBJECT_NOT_FOUND if credentials were not found.
    - DB_ERROR otherwise.
  """
  try:
    return Tokens.objects.get(id = tokenId)
  except (Tokens.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == Tokens.DoesNotExist else DB_ERRORS[2]
  

#######################################
# Functions Related to login process. # 
#######################################

def checkLoginCredentials(email, password, macAddress):
  """
  This function check shop assistant credentials and device MAC address.
  Returns:
    - A token if the shop assistant and device are registered in CEES database.
    - OBJECT_NOT_FOUND if credentials were not found.
    - DB_ERROR if token could not be saved in CEES database.
  """
  try:
    shopAssistant = ShopAssistants.objects.get(email = email, password = password) # Checking shop assistant credentials.
    device = Devices.objects.get(mac_address = macAddress)                         # Checking device mac address.
    token = Tokens(id = str(uuid.uuid4()), creation_datetime = str(datetime.now()), sa = shopAssistant, device = device)    # Creating a new token and saving it.
    token.save()
  except (ShopAssistants.DoesNotExist, Devices.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == ShopAssistants.DoesNotExist or type(dbe) == Devices.DoesNotExist else DB_ERRORS[2]
  return token.id

def deleteToken(tokenId):
  """
  This function deletes the token making the shop assistant log out.
  Returns:
    - SUCC_QUERY if token could be deleted.
    - DB_ERROR otherwise.
  """
  try:
    Tokens.objects.filter(id = tokenId).delete()
  except Error as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2]
  return DB_ERRORS[0]

def getStores(customer):
  """
  This function returns the stores linked to the given customer.
  This function does not care about token, it is done before.
  Returns the Stores in case of success, otherwise will return an error (OBJECT_NOT_FOUND if the store was not found, DB_ERROR otherwise).
  """
  try:
    storeList = Stores.objects.get(customer = customer) 
    stores = {}
    cities = []
    for store in storeList:
      cities.append(store.city)
      stores[store.city] = store.address
    stores[c.CITIES] = set(cities)
    return stores
  except (Stores.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe) 
    return DB_ERRORS[1] if type(dbe) == Stores.DoesNotExist else DB_ERRORS[2]

#########################################
# Functions Related to checkin process. # 
#########################################

def checkIn(token, regId, store):
  """
  This function will persist the checkin in the database.
  If an error occurs will raise a DB_ERROR.
  """
  try:
    CheckIns(token = token, registration = regId, store = store, date_time = str(datetime.now())).save()
  except Error as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2]
  return DB_ERRORS[0]

def checkOut(token):
  """
  This function will check out a shop assistant by deleting the entry linked to the given token.
  Returns SUCC_QUERY if success, DB_ERROR otherwise.
  """
  try:
    CheckIns.objects.filter(token = token).delete()
  except Error as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2]
  return DB_ERRORS[0]

def getRegistrationId(device):
  """
  This function returns the registration ID linked to a given device.
  If there is no registration linked to the device will return a OBJECT_NOT_FOUND error.
  Other error will raise a DB_ERROR.
  """
  try:
    return SaRegistrations.objects.get(device = device)
  except (SaRegistrations.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == SaRegistrations.DoesNotExist else DB_ERRORS[2] 

def getStore(city, address):
  """
  This function returns the store linked to a given city and address.
  If there is no store will return a OBJECT_NOT_FOUND error.
  Other error will raise a DB_ERROR.
  """
  try:
    return Stores.objects.get(city = city, address = address)
  except (Stores.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == SaRegistrations.DoesNotExist else DB_ERRORS[2]

def getDevice(tokenId):
  """
  This function returns the device linked to the given token.
  This function does not care about token authentication, it is done before.
  Returns the Shop Assistant ID in case of success, otherwise will return an error.
  """
  try:
    return Tokens.objects.get(id = tokenId).device
  except (Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2] 

def getShopAssistant(tokenId):
  """
  This function returns the shop assistant linked to the given token.
  This function does not care about token authentication, it is done before.
  Returns the Shop Assistant ID in case of success, otherwise will return an error.
  """
  try:
    return Tokens.objects.get(id = tokenId).sa
  except (Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2] 

def getCustomer(saId):
  """
  This function returns the customer linked to the given shop assistant.
  This function does not care about if the shop assistant exists, it is done before.
  Returns the Customer ID in case of success, otherwise will return an error.
  """
  try:
    return ShopAssistants.objects.get(id = saId).customer
  except (Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2]

#########################################
# Functions Related to client arrivals. #  
######################################### 

def getClientFromRFID(rfid):
  """
  This function returns the client linked to the given rfid.
  It will raise a OBJECT_NOT_FOUND error in case of the RFID card does not exist, DB_ERROR otherwise.
  """
  try:
    return RfidCards.objects.get(id = rfid).client
  except (RfidCards.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == RfidCards.DoesNotExist else DB_ERRORS[2]


def getCustomerFromId(customerId):
  try:
    Customers.objects.get(id = customerId)
  except (Clients.DoesNotExist, Error) as dbe:
    dblogger(dbe)
    return DB_ERRORS[1] if type(dbe) == RfidCards.DoesNotExist else DB_ERRORS[2]

def getStoreFromId(storeId):
  """
  This function returns the store linked to a given city and address.
  If there is no store will return a OBJECT_NOT_FOUND error.
  Other error will raise a DB_ERROR.
  """
  try:
    return Stores.objects.get(id = storeId)
  except (Stores.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == SaRegistrations.DoesNotExist else DB_ERRORS[2]

def saveArrival(client, store):
  """
  This function persists the client arrival.
  Return SUCC_QUERY in case of success, DB_ERROR otherwise.
  """
  try:
    ClientArrivals(client = client, store = store, status = c.AWAITING, datetime = str(datetime.now()), url = "https://localhost/clients/" + str(client.id) + "/" + str(client.id) + ".jpeg").save()
    return DB_ERRORS[0]
  except Error as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2]

def getRegistrationIds(store):
  """
  This function returns the registration ids list from shop assistants who have checked into a given store.
  """
  try:
    regIds = []
    for r in (CheckIns.objects.filter(store = store).values(c.REGISTRATIONID)):
      regIds.append(r[c.REGISTRATIONID])
    return regIds
  except (CheckIns.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == CheckIns.DoesNotExist else DB_ERRORS[2]