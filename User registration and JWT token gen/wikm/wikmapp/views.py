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


@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def checkAllergies(request):
    user = request.user 
    data=run() ##runs the barcode scanner and returns data associated with it.
    allergies = check_for_allergens(data)
    return JsonResponse({'allergies': allergies}) #returns what the user is allergic to in the product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_img_path(request,path): #set the path for the image.
    user = request.user
    GetProdData.set_img()
    return Response("path set")