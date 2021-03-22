from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User


class PutchUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'bio', 'role')
        model = User


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ('email',)


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    confirmation_code = serializers.CharField(write_only=True,
                                              allow_blank=False)

    class Meta:
        model = User
        fields = ('confirmation_code', 'email',)
