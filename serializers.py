"""
File: serializers.py
Author: Fernando Crespo Gravalos (cees.project.official@gmail.com)
Date: 2014/06/22 
"""

from rest_framework import serializers
from cees.models import Clients

class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Clients 
    fields = ('name', 'surname', 'age', 'sex')
    