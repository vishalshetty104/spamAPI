from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .serializer import UserSerializer,GlobalDbSerializer, PhoneTokenSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User,GlobalDb

# Create your views here.

class Register(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'new user registered successfully'
            data['phone'] = user.phone
            data['name'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data,status=200)

class Spam(generics.UpdateAPIView):

    def put(self, request, *args, **kwargs):
        phone_no = request.data.get('phone')
        if phone_no is None:
            return Response({"Phone number not found"}, status=404)
        try:
            numbers = GlobalDb.objects.filter(phone_no=phone_no)
            for number in numbers:
                number.is_spam = True
                number.save()
            response_data = {number.phone_no + " has been reported. Thank you"}
            return Response(response_data,status=200)
        except:
            response_data = {phone_no + " doesn't exist"}
            return Response(response_data,status=404)

class Login(ObtainAuthToken):
    permission_classes = (AllowAny,)
    serializer_class = PhoneTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({'token':token.key}, status=200)


class SearchName(APIView):

    permission_classes = (IsAuthenticated, )
    def get(self, request):
        name = request.data.get('name')
        startswith = GlobalDb.objects.filter(name__istartswith = name)
        contains = GlobalDb.objects.filter(name__contains = name).exclude(name__startswith = name) #exclude results that we get in startswith
        startswith_data = GlobalDbSerializer(startswith,many=True)
        contains_data = GlobalDbSerializer(contains, many=True)
        return Response(startswith_data.data+contains_data.data, status=200)

class SearchNumber(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self,request):
        phone_no = request.data.get('phone')
        try: #searches for registered user and displays only that if found
            user = GlobalDb.objects.get(phone_no=phone_no, is_registered=True)
            serializer = GlobalDbSerializer(user)
        except:
            user = GlobalDb.objects.filter(phone_no=phone_no)
            if not user:
                return Response({"Phone number is required"}, status=404)
            serializer = GlobalDbSerializer(user, many=True)

        return Response(serializer.data, status=200)

