"""
File: ceesvalidator.py
Author: Fernando Crespo Gravalos
Date: 2014/06/4
"""

import json
from jsonschema import validate, ValidationError
from os import path
from ceesloggers import getCeesAppLogger 

class CeesValidator:
  """
  This class is in charge of validate data sent to CEES Web Service.
  """
  def __init__(self):

    self.LOGIN_SCHEMA = path.abspath('schemas/loginschema.json')
    self.CHECKIN_SCHEMA = path.abspath('schemas/checkinschema.json')
    self.DETECTION_SCHEMA = path.abspath('schemas/detectionschema.json')
    self.CLIENT_INFO_SCHEMA = path.abspath('schemas/clientinfoschema.json')
    self.SCHEMA_CODES = {'LOGIN' : self.LOGIN_SCHEMA, 'CHECKIN' : self.CHECKIN_SCHEMA, 'DETECTION' : self.DETECTION_SCHEMA, 'CLIENT_INFO' : self.CLIENT_INFO_SCHEMA}
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
      return 1 if type(ve) == IOError else 2
    return 0
