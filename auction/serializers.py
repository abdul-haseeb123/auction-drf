from rest_framework import serializers
from auction.models import User, Listing, Bid


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'email_verified', 'first_name', 'last_name', 'avatar', 'cover', 'account_type', 'password']\
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Update the user fields
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # If a new password is provided, set it
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Hash the new password

        instance.save()
        return instance
    
