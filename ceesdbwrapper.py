"""
File: ceesdbwrapper.py
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/05
"""
"""
This script wraps queries to data model (CEES database).
This keeps the view handling requests and responses.
"""

###################################################################
# set-up to run a model query from ceesdbwrapper. 
###################################################################
from os import path as os_path, environ
from sys import path as sys_path
sys_path.append(os_path.abspath(os_path.join(os_path.dirname(__file__), os_path.pardir)))
environ.setdefault("DJANGO_SETTINGS_MODULE", "cees.settings")
####################################################################
import uuid
from django.db import Error
from cees.models import ShopAssistants, Tokens, Devices, Stores
from ceesloggers import getDbLogger 

dblogger = getDbLogger()

"""
Authorization
"""

def checkToken(tokenId):
  """
  This function checks that the token given in Authorization Header is present in CEES database.
  Returns:
    - A token if the shop assistant and device are registered in CEES database.
    - 0 if credentials were not found.
    - 1 if token could not be saved in CEES database.
  """
  try:
    Tokens.objects.get(id = tokenId)
  except (Tokens.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return 1 if type(dbe) == Tokens.DoesNotExist else 2
  return 0

"""
Functions related to login process.
"""

def checkLoginCredentials(email, password, macAddress):
  """
  This function check shop assistant credentials and device MAC address.
  Returns:
    - A token if the shop assistant and device are registered in CEES database.
    - 0 if credentials were not found.
    - 1 if token could not be saved in CEES database.
  """
  try:
    shopAssistant = ShopAssistants.objects.get(email = email, password = password) # Checking shop assistant credentials.
    device = Devices.objects.get(mac_address = macAddress)                         # Checking device mac address.
    token = Tokens(id = str(uuid.uuid4()), sa = shopAssistant, device = device)    # Creating a new token and saving it.
    token.save()
  except (ShopAssistants.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return 0 if type(dbe) == ShopAssistants.DoesNotExist else 1
  return token.id

def deleteToken(tokenId):
  """
  This function deletes the token making the shop assistant log out.
  Returns:
    - 0 if token could be deleted.
    - 1 otherwise.
  """
  try:
    Tokens.objects.filter(id = tokenId).delete()
  except Error as dbe:
    dblogger.exception(dbe)
    return 1
  return 0

def getStores(tokenId):
  """
  This function returns the st
  """
  try:
   sa = Tokens.objects.get(id = tokenId).sa
   customer = ShopAssistants.objects.get(sa = sa).customer
   return Stores.objects.get(customer = customer).city
  except (Tokens.DoesNotExist, ShopAssistants.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return 0 if type(dbe) == Tokens.DoesNotExist else 1 # If shop assistant is not found should be an internal error, since this function is called aferter login

def getShopAssistantId(tokenId):
  """
  This function returns the shop assistant linked to a given a token.
  Returns -1 in case of error.
  """
  try:
    return Tokens.objects.get(id = tokenId).saId
  except (Tokens.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return -1 # 

def getCustomerId(saId):
  try:
    return ShopAssistants.objects.get(id = saId).customer.id
  except(ShopAssistants.DoesNotExists, Error) as dbe:
    dblogger.exception(dbe)
    return -1


