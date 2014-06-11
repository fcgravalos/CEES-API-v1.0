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
import constants as c
from datetime import datetime
from django.db import Error
from cees.models import ShopAssistants, Tokens, Devices, Stores
from ceesloggers import getDbLogger 


dblogger = getDbLogger()
DB_ERRORS = { 0 : c.SUCC_QUERY, 1 : c.OBJECT_NOT_FOUND, 2 : c.DB_ERROR}

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
    return DB_ERRORS[1] if type(dbe) == Tokens.DoesNotExist else DB_ERRORS[2]
  return DB_ERRORS[0]

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
    token = Tokens(id = str(uuid.uuid4()), creation_datetime = str(datetime.now()), sa = shopAssistant, device = device)    # Creating a new token and saving it.
    token.save()
  except (ShopAssistants.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[1] if type(dbe) == ShopAssistants.DoesNotExist else DB_ERRORS[2]
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
    return DB_ERRORS[2]
  return DB_ERRORS[0]

def getStores(customer):
  """
  This function returns the stores linked to the given customer.
  This function does not care about token, it is done before.
  Returns the Stores in case of success, otherwise will return an error.
  """
  try:
    storeList = Stores.objects.filter(customer = customer)
    stores = {}
    cities = []
    for store in storeList:
      cities.append(store.city)
      stores[store.city] = store.address
    stores['cities'] = set(cities)
    return stores
  except (Stores.DoesNotExist, Error) as dbe:
    dblogger.exception(dbe) 
    return DB_ERRORS[1] if type(dbe) == Stores.DoesNotExist else DB_ERRORS[2]
    
     

def getShopAssistant(tokenId):
  """
  This function returns the shop assistant linked to the given token.
  This function does not care about token, it is done before.
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
  except(Error) as dbe:
    dblogger.exception(dbe)
    return DB_ERRORS[2] 


