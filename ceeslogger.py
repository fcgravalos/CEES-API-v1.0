"""
File: ceesloggers.py 
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date : 06/Jun/2014
"""
"""
This script encapsulates logger names and calls.
This will make the code cleaner.
"""

from logging import getLogger

#Logger names.
REQUEST_LOGGER = 'django.request'
DB_LOGGER = 'django.db'
CEES_APPLICATION_LOGGER = 'cees.app'

def getRequestLogger():
  """
  This function will return the logger for HTTP requests.
  """
  return getLogger(REQUEST_LOGGER)
  
def getDbLogger():
  """
  This function will return the logger for CEES database queries.
  """
  return getLogger(DB_LOGGER)
  
def getCeesAppLogger():
  """
  This function will return the logger for CEES application events.
  """
  return getLogger(CEES_APPLICATION_LOGGER)

