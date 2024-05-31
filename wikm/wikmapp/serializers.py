from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import Allergy
from .models import Child


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AllergySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Allergy
        fields = ['id', 'name', 'user', 'child']

class ChildSerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)

    class Meta:
        model = Child
        fields = ['id', 'name', 'allergies']

class ProfileSerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)
    children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'allergies', 'children']
