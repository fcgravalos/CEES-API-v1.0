from rest_framework import serializers
from cees.models import Tokens, Stores

class TokensSerializer(serializers.Serializer):

  id = serializers.CharField()
  sa = serializers.IntegerField()
  device = serializers.IntegerField()

class StoresSerializer(serializers.Serializer):
	id = serializers.IntegerField()
    city = serializers.CharField()
    address = serializers.CharField()
    telephone = serializers.CharField()
    email = serializers.CharField()
    customer = serializers.ForeignKey()
    status = serializers.CharField()