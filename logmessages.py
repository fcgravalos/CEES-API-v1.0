"""
File: logmessages.py  
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/16
"""
##############
# LOG MESSAGES
##############

## GENERAL ##
DB_ERROR = 'Database error. Check database log file.'
STORE_NOT_FOUND = 'Could not find store in cees database.'
TOKEN_NOT_FOUND = 'Could not find token in database.'
SCHEMA_NOT_FOUND = 'Could not validate request. Schema file not found.'
VALIDATION_ERROR = 'Data not valid.'

## LOGIN ##
LOGGED_IN = 'Shop assistant logged in as '
CREDENTIALS_NOT_FOUND = 'Could not find the email/password provided.'

## ARRIVALS ##
RFID_NOT_FOUND = 'Invalid identifier. RFID not found in cees database.'
CLIENT_NOT_ALLOWED = 'Client does not belong to this customer.'
SENDING_NOTIFICATION = 'Sending push notification.'
CLIENT_NOT_FOUND = 'Client not found as an arrival.'

## TOKEN ##
MISSING_TOKEN = 'There is no Authentication header in request.'

## GCM AND DEVICE REGISTRATION##
UNKNOWN_DEVICE = 'Device not found in databse.'
REGISTRATION_NOT_FOUND = 'Registration not found in database.'