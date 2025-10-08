from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Availability

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class AvailabilitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    class Meta:
        model = Availability
        fields = ['id','user','user_id','date','time_slot','status','note']
