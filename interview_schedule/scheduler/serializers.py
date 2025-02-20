import re
import logging

from rest_framework import serializers
from .models import UserDetails

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetails
        fields = ['user_id','user_name','user_type','user_mail','time_slot_from','time_slot_to']

        # validating the user id
        def validate_user_id(self, value):
            if not value.strip():
                raise serializers.ValidationError("User ID cannot be empty.")
            return value
        
        # validating the name
        def validate_user_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            if value.isdigit():
                raise serializers.ValidationError("Name cannot be a numeric value.")
            return value
        
        # validating the provided user type
        def validate_user_type(self,value):
            if not value.strip():
                raise serializers.ValidationError("User type cannot be empty.")
            if value not in ['interviewer','candidate']:
                raise serializers.ValidationError("Invalid User Type")
            return value
        
        # validating the provided email of user using regular expression
        def validate_user_mail(self, value):
            if not value.strip():
                raise serializers.ValidationError("Email cannot be empty.")
            
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                raise serializers.ValidationError("Invalid email address")
            else:
                return value
        
        # validating the 'time_slot_from' based on office starting
        def validate_time_slot_from(self, value):
            if not value.strip():
                raise serializers.ValidationError("Time slot from cannot be empty.")
            
            if value.isalpha():
                raise serializers.ValidationError("Time slot from cannot be alphabetic.")
            
            return value
        
        # validating 'time_slot_to' to ensure it is > 'time_slot_from'
        def validate_time_slot_to(self, value):

            if not value.strip():
                raise serializers.ValidationError("Time slot to cannot be empty.")
            
            if value.isalpha():
                raise serializers.ValidationError("Time slot to cannot be alphabetic.")
            
            return value
