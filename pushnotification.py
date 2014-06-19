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

def sendNotification(registrationIds, client):
	gcm = GCM(c.GCM_API_KEY)
	data = {c.EVENT : "New arrival: " + client.name + " " + client.surname}
	print gcm.json_request(registration_ids = registrationIds, data = data)
