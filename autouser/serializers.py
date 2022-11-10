from rest_framework import serializers
from django.contrib.auth import get_user_model

from autouser.models import AutoUserFavourite

User = get_user_model()


class RegisterAutoUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            is_technician=False,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'photo', 'email', 'password', 'is_technician',
        )
        extra_kwargs = {'password': {'write_only': True}, 'is_technician': {'read_only': True}}


class AutoUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AutoUserFavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoUserFavourite
        fields = '__all__'
        depth = 1
