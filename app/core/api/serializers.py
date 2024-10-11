from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        
    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)
    
    
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.set_password(validated_data.get('password', instance.password))
    #     instance.save()
    #     return instance
            
    # updating our user serializer
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=5, style={
        "input_type": "password",
    }, trim_whitespace=False,)
    
    
    def validate(self, data):
        """
            Validate and Authenticate User
        """
        email = data.get('email')   # retrieve data
        password = data.get('password')
        
        if email is None and password is None:
            raise serializers.ValidationError({'error': 'Please enter a valid email and password'})
        
        user = authenticate(
                            request=self.context.get('request'), 
                            username= email,
                            password = password)
        
        if not user:
            message = _("Unable to authenticate with Provided credentials")
            raise serializers.ValidationError(message, code='authorization')
        
        data['user'] = user 
        return data
    
    