"""
File: views.py
Author: Fernando Crespo Gravalos for CEES. (cees.project.official@gmail.com)
Date: 2014/06/05
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import ceesresponse as cr
import ceesvalidator as cv
import ceesdbwrapper as cdbw
import constants as c
import logmessages as lm
import pushnotification as pn
import requesthandler as rh
from ceesloggers import getCeesAppLogger

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
    (response, stores) = rh.getStores(request)
    if response == c.UNAUTHORIZED:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED) 
    elif response == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif response == c.NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 4, ''), status = status.HTTP_404_NOT_FOUND)
    return Response(cr.CeesResponse().getCeesResponse(0, 0, stores), status = status.HTTP_200_OK)

    
  def post(self, request):
    """
    Login shop assistants. If email and password matches returns a token.   
    """
    response = rh.login(request)
    (status_code, tokenId) = response 
    if status_code == c.BAD_REQUEST: # Validation error.
      return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST) # JSON format not valid or data parsing failed.
    elif status_code == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR) # Internal Error.
    elif status_code == c.UNAUTHORIZED:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED) # Credentials not found.
    else:
      return Response(cr.CeesResponse().getCeesResponse(0, 0, tokenId), status = status.HTTP_201_CREATED) # Token created.

  def delete(self, request):
    """
    Logout. This will delete token from database.
    """
    response = rh.logout(request)
    if response == c.UNAUTHORIZED:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif response == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR) # Database error. Returns HTTP 500.
    return Response(cr.CeesResponse().getCeesResponse(0, 0, ''), status = status.HTTP_200_OK) # Ok. Returns HTTP 200.
    
class CheckinView(APIView):
  """
  This class encapsulates check-in process: check into a store and check-out.
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
    response = rh.checkin(request)
    if response == c.UNAUTHORIZED:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif response == c.BAD_REQUEST:
      return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST)
    elif response == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif response == c.NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_404_NOT_FOUND)
    return Response(cr.CeesResponse().getCeesResponse(0 , 0, ''), status = status.HTTP_201_CREATED) # Checkin persisted. HTTP 201.


  def delete(self, request):
    """
    This function will check out a shop assistant from a store.
    """
    response = rh.checkout(request)
    if response == c.UNAUTHORIZED:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    elif response == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(cr.CeesResponse().getCeesResponse(0 , 0, ''), status = status.HTTP_200_OK)

class ArrivalView(APIView):
  """
  This class encapsulates the arrivals: incoming arrival, getting information about a client and so on.
  - To set a new arrival, send a POST in the same way that the detection system does:

    {"customerID" : your_customer_id, "storeID" : your_store_id, "rfid" : "rfid_card"}
  """
  def post(self, request):
    """
    Store a new arrival with the incoming request from detection system.
    """
    response = rh.newArrival(request)
    if response == c.BAD_REQUEST:
      return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST) # Validation Error. Returns HTTP 400.
    elif response == c.NOT_FOUND:
      return Response(cr.CeesResponse().getCeesResponse(1, 4, ''), status = status.HTTP_404_NOT_FOUND)
    elif response == c.FORBBIDEN:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_403_FORBIDDEN)
    elif response == c.INTERNAL_SERVER_ERROR:
      return Response(cr.CeesResponse().getCeesResponse(1 , 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(cr.CeesResponse().getCeesResponse(0 , 0, ''), status = status.HTTP_201_CREATED)








