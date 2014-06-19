"""
File: constants.py
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/10
"""

##########
# SETTINGS
##########
DJANGO_SETTINGS = 'DJANGO_SETTINGS_MODULE'
CEES_SETTINGS = 'cees.settings'

##############
# HTTP HEADERS
##############
AUTHENTICATION = 'HTTP_AUTHENTICATION'

###################
# HTTP STATUS CODES
###################
OK = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBBIDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500

########################
# SCHEMAS RELATIVE PATHS
########################
LOGIN_SCHEMA_PATH = 'schemas/loginschema.json'
CHECKIN_SCHEMA_PATH = 'schemas/checkinschema.json'
DETECTION_SCHEMA_PATH = 'schemas/detectionschema.json'
CLIENT_INFO_SCHEMA_PATH = 'schemas/clientinfoschema.json'

########################
# SCHEMAS FILTERING KEYS
########################
LOGIN = 'LOGIN'
CHECKIN = 'CHECKIN'
DETECT = 'DETECTION'
CLIENT = 'CLIENT_INFO'

#######################
# VALIDATION ERROR KEYS
#######################
VALID_SUCC = 'VALIDATION_SUCCESSFUL'
IOERR = 'IO_ERROR'
VALID_ERR = 'VALIDATION_ERROR'

#####################
# DATABASE ERROR KEYS
#####################
SUCC_QUERY = 'SUCCESSFUL_QUERY'
OBJECT_NOT_FOUND = 'OBJECT_NOT_FOUND' 
DB_ERROR = 'DATABASE_GENERAL_ERROR'

#################
# LOGIN DATA KEYS
#################
EMAIL = 'email'
PASSWORD = 'password'
MAC_ADDRESS = 'macAddress'

###################
# CHECKIN DATA KEYS
###################
CITIES = 'cities'
CITY = 'city'
ADDRESS = 'address'

###################
# ARRIVAL DATA KEYS
###################
AWAITING = 'AWAITING'
CUSTOMERID = 'customerID'
STOREID = 'storeID'
RFID = 'rfid'

####################################
# GCM SETTINGS---move to settings.py
####################################
GCM_API_KEY = 'AIzaSyDuvrfGOwLsb2tgu-6oa2T06oPDAIHrUq8'
EVENT = 'EVENT'
REGISTRATIONID = 'registration'