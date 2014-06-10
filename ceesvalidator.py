"""
File: ceesvalidator.py
Author: Fernando Crespo Gravalos
Date: 2014/06/4
"""

import json
from jsonschema import validate, ValidationError
from os import path
from ceesloggers import getCeesAppLogger 
import constants as c

class CeesValidator:
  """
  This class is in charge of validate data sent to CEES Web Service.
  """
  def __init__(self):

    self.LOGIN_SCHEMA = path.abspath(c.LOGIN_SCHEMA_PATH)
    self.CHECKIN_SCHEMA = path.abspath(c.CHECKIN_SCHEMA_PATH)
    self.DETECTION_SCHEMA = path.abspath(c.DETECTION_SCHEMA_PATH)
    self.CLIENT_INFO_SCHEMA = path.abspath(c.CLIENT_INFO_SCHEMA_PATH)
    self.SCHEMA_CODES = {c.LOGIN : self.LOGIN_SCHEMA, c.CHECKIN : self.CHECKIN_SCHEMA, c.DETECT : self.DETECTION_SCHEMA, c.CLIENT : self.CLIENT_INFO_SCHEMA}
    self.VALIDATION_ERRORS = {0 : c.VALID_SUCC, 1 : c.IOERR, 2 : c.VALID_ERR}
    self.applogger = getCeesAppLogger()

  def validate(self, data, schemaCode):
    """
    Validates the data against the selected schema.
    Returns: 
      - 1 if an IOError is raised.
      - 2 if a Validation error is raised.
      - 0 if no exception is raised.
    """
    selected_schema = self.SCHEMA_CODES[schemaCode] # Filter the right schema.
    try:
      with open(selected_schema) as schema_file:
        schema = json.loads(schema_file.read())
      validate(data, schema)
    except (IOError, ValidationError) as ve:
      self.applogger.exception(ve)     
      return self.VALIDATION_ERRORS[1] if type(ve) == IOError else self.VALIDATION_ERRORS[2]
    return self.VALIDATION_ERRORS[0]
