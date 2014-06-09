# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class CheckIns(models.Model):
    token = models.ForeignKey('Tokens', unique=True)
    store = models.ForeignKey('Stores')
    registration = models.ForeignKey('SaRegistrations', db_column='registration_ID', blank=True, null=True) # Field name made lowercase.
    date_time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'check_ins'

class ClientArrivals(models.Model):
    client = models.ForeignKey('Clients')
    store = models.ForeignKey('Stores')
    datetime = models.DateTimeField()
    status = models.CharField(max_length=8)
    url = models.CharField(max_length=45, blank=True)
    class Meta:
        managed = False
        db_table = 'client_arrivals'

class Clients(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45, blank=True)
    email = models.CharField(max_length=45)
    age = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    telephone = models.CharField(max_length=45, blank=True)
    customer = models.ForeignKey('Customers')
    external_id = models.CharField(max_length=45, blank=True)
    isactive = models.CharField(db_column='isActive', max_length=3) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'clients'

class ContactPoints(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45, blank=True)
    telephone = models.CharField(unique=True, max_length=45)
    email = models.CharField(unique=True, max_length=45)
    store = models.ForeignKey('Stores', blank=True, null=True)
    customer = models.ForeignKey('Customers', db_column='customer_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'contact_points'

class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    social_address = models.CharField(unique=True, max_length=45)
    contactpoint_id = models.CharField(db_column='ContactPoint_ID', unique=True, max_length=45, blank=True) # Field name made lowercase.
    billing_address = models.CharField(db_column='Billing_Address', unique=True, max_length=45) # Field name made lowercase.
    billing_cc = models.CharField(db_column='Billing_CC', unique=True, max_length=45) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'customers'

class Devices(models.Model):
    id = models.IntegerField(primary_key=True)
    mac_address = models.CharField(unique=True, max_length=45)
    class Meta:
        managed = False
        db_table = 'devices'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class IpCameras(models.Model):
    id = models.IntegerField(primary_key=True)
    ip_address = models.CharField(max_length=17)
    model = models.CharField(max_length=45, blank=True)
    store = models.ForeignKey('Stores', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ip_cameras'

class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    description = models.IntegerField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    subcategory = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(Customers)
    internal_code = models.CharField(max_length=45, blank=True)
    class Meta:
        managed = False
        db_table = 'products'

class ProductsPurchase(models.Model):
    purchase = models.ForeignKey('Purchases', db_column='purchase_ID') # Field name made lowercase.
    product = models.ForeignKey(Products)
    cantidad = models.CharField(max_length=45)
    ispurchasable = models.IntegerField(db_column='IsPurchasable') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'products_purchase'

class Projects(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=15)
    customer = models.ForeignKey(Customers)
    class Meta:
        managed = False
        db_table = 'projects'

class Purchases(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=45)
    time = models.DateTimeField(blank=True, null=True)
    shop_assistant = models.ForeignKey('ShopAssistants', db_column='shop_assistant')
    store = models.ForeignKey('Stores', blank=True, null=True)
    invoice_id = models.CharField(max_length=45, blank=True)
    class Meta:
        managed = False
        db_table = 'purchases'

class RfidCards(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    other_info = models.CharField(max_length=45, blank=True)
    status = models.CharField(max_length=9)
    client = models.ForeignKey(Clients, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rfid_cards'

class SaRegistrations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    device = models.ForeignKey(Devices)
    class Meta:
        managed = False
        db_table = 'sa_registrations'

class ShopAssistantShifts(models.Model):
    shop_assistant = models.ForeignKey('ShopAssistants')
    store = models.ForeignKey('Stores')
    date_in = models.DateTimeField()
    data_time_out = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'shop_assistant_shifts'

class ShopAssistants(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    telephone = models.CharField(max_length=45)
    internal_code = models.CharField(max_length=45)
    hiring_date = models.CharField(max_length=45, blank=True)
    customer = models.ForeignKey(Customers)
    status = models.CharField(max_length=9, blank=True)
    class Meta:
        managed = False
        db_table = 'shop_assistants'

class Stores(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=45, blank=True)
    address = models.CharField(unique=True, max_length=45)
    telephone = models.CharField(unique=True, max_length=45, blank=True)
    email = models.CharField(unique=True, max_length=45, blank=True)
    customer = models.ForeignKey(Customers)
    status = models.CharField(max_length=8, blank=True)
    def __unicode__(self): 
        return self.city
    class Meta:
        managed = False
        db_table = 'stores'

class Tokens(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    sa = models.ForeignKey(ShopAssistants, db_column='SA_id') # Field name made lowercase.
    creation_datetime = models.DateTimeField(db_column='creation_dateTime') # Field name made lowercase.
    device = models.ForeignKey(Devices, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tokens'

