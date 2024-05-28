from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from django.utils import timezone
from .serializers import ProfileSerializer
from .isallergic import *
from .GetProdData import *
from .models import Allergy
from .serializers import *
from django.http import JsonResponse
from .prodFunctions import GetProdData

# Create your views here.

def getRoutes(request):
    return HttpResponse("getRoutes test view")

def home(request):
    return HttpResponse("homepage test view")

# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def perform_create(self, serializer):
        # Call the parent's perform_create method to create the token
        data = super().perform_create(serializer)
        
        # Update the last_login field of the user
        user = User.objects.get(username=self.request.data.get('username'))
        user.last_login = timezone.now()
        user.save()
        
        return data

    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate user credentials
        user = authenticate(username=username, password=password)

        if user:
            # Generate tokens if credentials are valid
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        else:
            # Return an error response if credentials are invalid
            return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
# Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkAllergies(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))  # Assuming JSON data is sent in the request body
    barcode = data.get('barcode', '')  # Retrieve barcode from JSON data
    prodData = GetProdData(barcode)
    
    return Response(prodData)



# Save multiple allergies to profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setAllergies(request):
    user = request.user
    allergy_names = request.data.get('allergies', [])

    if not isinstance(allergy_names, list):
        return Response({"detail": "Allergies should be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)

    # Delete all existing allergies for the user
    Allergy.objects.filter(user=user).delete()

    created_allergies = []

    for allergy_name in allergy_names:
        # Create a new allergy
        allergy = Allergy.objects.create(user=user, name=allergy_name)
        serializer = AllergySerializer(allergy)
        created_allergies.append(serializer.data)

    return Response(created_allergies, status=status.HTTP_200_OK)

#get allergy from profie
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserAllergies(request):
    user = request.user
    allergies = Allergy.objects.filter(user=user)
    serializer = AllergySerializer(allergies, many=True)
    return Response(serializer.data)

