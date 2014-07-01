"""
File: pushnotification.py 
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/17
"""
"""
Interface with Google Cloud Messaging API.
"""
from gcm import GCM
import constants as c
import ceesdbwrapper as cdbw
from ceesloggers import getCeesAppLogger

applogger = getCeesAppLogger()


def sendNotification(registrationIds, client):
  gcm = GCM(c.GCM_API_KEY)
  data = {c.EVENT : "New arrival: " + client.name + " " + client.surname}
  response = gcm.json_request(registration_ids = registrationIds, data = data)
  gcmErrorHandling(response)  

def gcmErrorHandling(response):
  if 'errors' in response:
    for error, reg_ids in response['errors'].items():
      applogger.error(error)                                
      # Remove reg_ids from database
      for reg_id in reg_ids:
        cdbw.deleteRegistrationId(reg_id)
  if 'canonical' in response:
    for reg_id, canonical_id in response['canonical'].items():
      applogger.warning('updating')
      cdbw.updateRegistrationId(reg_id, canonical_id)
