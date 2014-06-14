"""
File: views.py
Author: Fernando Crespo Gravalos for CEES. (cees.project.official@gmail.com)
Date: 2014/06/05
"""
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import ceesresponse as cr
import ceesvalidator as cv
import ceesdbwrapper as cdbw
import constants as c 

class LoginView(APIView):
  """
  This class encapsulate login process: login, get store list and logout.
  It handles login requests, validates it, processes it and respond.

  - To login send a POST request with content type JSON. The payload should be:
  
      {"email" : "shop_assistant_email", "password" : "shop_assistant_password", "macAddress" : "device_MAC_Address"}
  
      This will return a token.
  
  - To logout send a DELETE request with an Authentication header containing the token retrieved in the login.

  - To get the stores send a GET request with an Authentication header containing the token retrieved in the login.
  """

  def get(self, request):
    """
    Gets the available stores (city and address) for a given shop asistant.
    """
    try:
      tokenId = request.META[c.AUTHENTICATION]
    except KeyError as re:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)

    token = cdbw.getToken(tokenId)
    if token == c.OBJECT_NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif token == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    sa = cdbw.getShopAssistant(tokenId)
    if sa == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    customer = cdbw.getCustomer(sa.id)
    if customer == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    stores = cdbw.getStores(customer.id)
    if stores == c.OBJECT_NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_404_INTERNAL_SERVER_ERROR)
    elif stores == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(cr.CeesResponse().getCeesResponse(0, 0, stores), status = status.HTTP_200_OK)
        
  def post(self, request):
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
        return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED) 
      elif auth == c.DB_ERROR: # Could not persist token. Returns HTTP 500.
        return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
      return Response(cr.CeesResponse().getCeesResponse(0, 0, auth), status = status.HTTP_201_CREATED) # Ok. Returns HTTP 201.
    elif validation_result == c.IOERR: # IOError. Returns HTTP 500.
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST) # Validation Error. Returns HTTP 400.

  def delete(self, request):
    """
    Logout. This will delete token from database.
    """
    try:
      if cdbw.deleteToken(request.META[c.AUTHENTICATION]) == c.SUCC_QUERY: 
        return Response(cr.CeesResponse().getCeesResponse(0, 0, ''), status = status.HTTP_200_OK) # Ok. Returns HTTP 200.
      else:
        return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR) # Database error. Returns HTTP 500.
    except KeyError as re: # If no Authentication header found, returns HTTP 401.
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    
class CheckinView(APIView):
  """
  This class encapsulate checkin process: checkin into a store and checkout.
  It handles checkin requests, validates it, processes it and responds.

  - To checkin send a POST request with content type JSON. Set the Authentication header with the token retrieved during the login. 
    The payload should be:
  
      {"city" : "store's city", "address" : "store's_address"}
  
      This will return a token.
  
  - To checkout send a DELETE request with an Authentication header containing the token retrieved during the login.
  """

  def post(self, request):  
    """
    Checkin shop assistant. Checks the authentication header and the city and address provided in the payload.
    """
    try:
      tokenId = request.META[c.AUTHENTICATION]
    except KeyError as re:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    
    token = cdbw.getToken(tokenId)
    if token == c.OBJECT_NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif token == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    sa = cdbw.getShopAssistant(tokenId)
    device = cdbw.getDevice(tokenId)
    if sa == c.DB_ERROR or device == c.DB_ERROR: # If there is no shop assistant or device linked to the token it's a database error.
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    regId = cdbw.getRegistrationId(device)
    if regId == c.OBJECT_NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_404_NOT_FOUND)
    elif regId == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    data = request.DATA # Parsing request. If it is malformed, Django will return HTTP 400 automatically.
    validationResult = cv.CeesValidator().validate(data, c.CHECKIN) # Validating request against schema.
    if validationResult == c.VALID_SUCC: # Validation successful. Extracting data.
      city = data.get(c.CITY)
      address = data.get(c.ADDRESS)
      store = cdbw.getStore(city, address)
      if store == c.OBJECT_NOT_FOUND: # Very rare. This is checking that the store was deleted after the login but before the checkin.
        return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_404_NOT_FOUND)
      elif store == c.DB_ERROR:
        return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
      else:
        if cdbw.checkIn(token, regId, store) != c.SUCC_QUERY:
          return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(cr.CeesResponse().getCeesResponse(0 , 0, ''), status = status.HTTP_201_CREATED) # Checkin persisted. HTTP 201.
    return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST) # Validation Error. Returns HTTP 400.
  

  def delete(self, request):
    """
    This function will check out a shop assistant from a store.
    """
    try:
      tokenId = request.META[c.AUTHENTICATION]
    except KeyError as re:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    token = cdbw.getToken(tokenId)
    if token == c.OBJECT_NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif token == c.DB_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if cdbw.checkOut(token) == c.SUCC_QUERY:
      return Response(cr.CeesResponse().getCeesResponse(0 , 0, ''), status = status.HTTP_200_OK)
    else:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)


