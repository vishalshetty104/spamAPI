from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User,GlobalDb

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone','username','password','email')

    def create(self, validated_data):
        user = User(phone=validated_data['phone'], username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        GlobalDb.objects.create(name=validated_data['username'], phone_no=validated_data['phone'], email=validated_data['email'], is_registered=True, user=user)

        return user


class GlobalDbSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalDb
        fields = ('name','phone_no','is_spam','is_registered')
        read_only_fields=('is_registered',)


class PhoneTokenSerializer(serializers.Serializer): #serializer for validating login info
    phone = serializers.CharField(write_only=True)
    password = serializers.CharField()

    def validate(self,data):
        phone = data.get('phone')
        password = data.get('password')
        user = get_user_model().objects.filter(phone=phone).first()
        if user:
            if user.check_password(password):
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid Password')
        else:
            raise serializers.ValidationError('Phone number is not registered')

        return data