"""
File: ceesresponse.py
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/04
"""
from datetime import datetime

class CeesResponse:
  """
  This class wraps the responses sent to customer device.
  The CEES Response contains:
   - Status: OK, NOK.
   - Root Cause: SUCCESS, INVALID_INPUT, AUTHENTICATION_FAILURE, INTERNAL_ERROR.
   - Timestamp: The current date time.
   - Data: The real message from server. Will be '' in case of error or CEES data otherwise.
  This isolates server errors and exception to the server. 
  """
  def __init__(self):
    self.STATUS_CODES = {0:'OK', 1:'NOK'}
    self.ROOT_CAUSE_CODES = {0 :'SUCCESS', 1 : 'INVALID_INPUT', 2 : 'AUTHENTICATION_FAILURE', 3 : 'INTERNAL_ERROR', 4 : 'NOT_FOUND'}

  def getCeesResponse(self, statusCode, rootCauseCode, data):
    """
    This function return the response given the status code, the root cause and the data.
    """
    status = self.STATUS_CODES[statusCode]
    rootCause = self.ROOT_CAUSE_CODES[rootCauseCode]
    return {'status' : status, 'root_cause' : rootCause, 'timestamp' : str(datetime.now()), 'data' : data}
