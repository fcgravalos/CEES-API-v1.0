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

class LoginView(APIView):
  """
  This class encapsulate login process: login, get store list and logout.
  It handles login requests, validate it, process it and respond. 
  """

  def get(self, request):
    """
    Get the available stores (city and address) for a given shop asistant.
    """
    try:
      tokenId = request.META['HTTP_AUTHENTICATION']
    except KeyError as re:
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)

    auth = cdbw.checkToken(tokenId)
    if auth == 0:

      return Response(cr.CeesResponse().getCeesResponse(0, 0, cdbw.getStores()))
        
    elif auth == 1:
      return Response(cr.CeesResponse().getCeesResponse(1, 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    else:
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(cr.CeesResponse().getCeesResponse(0, 0, cdbw.getStores()))

  def post(self, request):
    """
    Login shop assistants. If email and password matches returns a token.
    """
    data = request.DATA # Parsing request. If it is malformed, Django will return HTTP 400 automatically.
    validation_result = cv.CeesValidator().validate(data, 'LOGIN') # Validating request against schema.
    if validation_result == 0: # Validation successful. Extracting data.
      email = data.get('email', False)
      password = data.get('password', False)
      macAddress = data.get('macAddress', False)
      auth = cdbw.checkLoginCredentials(email, password, macAddress) # Checking credentials.
      if auth == 0: # Credentials not found. Returns HTTP 401.
        return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED) 
      elif auth == 1: # Could not persist token. Returns HTTP 500.
        return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
      return Response(cr.CeesResponse().getCeesResponse(0, 0, auth), status = status.HTTP_201_CREATED) # Ok. Returns HTTP 201.
    elif validation_result == 1: # IOError. Returns HTTP 500.
      return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(cr.CeesResponse().getCeesResponse(1, 1, ''), status = status.HTTP_400_BAD_REQUEST) # Validation Error. Returns HTTP 400.

  def delete(self, request):
    """
    Logout. This will delete token from database.
    """
    try:
      if cdbw.deleteToken(request.META['HTTP_AUTHENTICATION']) == 0: 
        return Response(cr.CeesResponse().getCeesResponse(0, 0, ''), status = status.HTTP_200_OK) # Ok. Returns HTTP 200.
      else:
        return Response(cr.CeesResponse().getCeesResponse(1, 3, ''), status = status.HTTP_500_INTERNAL_SERVER_ERROR) # Database error. Returns HTTP 500.
    except KeyError as re: # If no Authentication header found, returns HTTP 401.
      return Response(cr.CeesResponse().getCeesResponse(1 , 2, ''), status = status.HTTP_401_UNAUTHORIZED)
    

       
    
