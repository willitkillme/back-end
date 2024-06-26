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
from .models import Allergy
from .serializers import *
from .prodFunctions import GetProdData,check_for_allergens

def getRoutes(request):
    return HttpResponse("getRoutes test view")

def home(request):
    return HttpResponse("homepage test view")

# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def perform_create(self, serializer):
        data = super().perform_create(serializer)
        
        user = User.objects.get(username=self.request.data.get('username'))
        user.last_login = timezone.now()
        user.save()
        
        return data

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        else:
            return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

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
    barcode = str(request.query_params.get('barcode', ''))

    if len(barcode) < 13:
        zeros_needed = 13 - len(barcode)
        barcode =  '0' * zeros_needed+barcode

    prodData,name,all_nutrients = GetProdData(barcode)    
    
    allergies = Allergy.objects.filter(user=user)
    allergy_names = [allergy.name for allergy in allergies]

    matches=check_for_allergens(prodData,allergy_names)
    
    
    child_matches = []
    for child in user.children.all():
        child_allergies = [allergy.name for allergy in child.allergies.all()]
        child_match = check_for_allergens(prodData, child_allergies)
        child_matches.append({"child_name": child.name, "matches": child_match})
    
    
    return Response({
        "product_name":name,
        "barcode":barcode,
        "product_data": prodData,
        "nutrients":all_nutrients,
        "alergy_names":allergy_names,
        "allergen_matches": matches,
        "child_matches": child_matches
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setAllergies(request):
    user = request.user
    allergy_names = request.data.get('allergies', [])
    if not isinstance(allergy_names, list):
        return Response({"detail": "Allergies should be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)

    Allergy.objects.filter(user=user).delete()

    created_allergies = []

    for allergy_name in allergy_names:
        allergy = Allergy.objects.create(user=user, name=allergy_name)
        serializer = AllergySerializer(allergy)
        created_allergies.append(serializer.data)

    return Response(created_allergies, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserAllergies(request):
    user = request.user
    allergies = Allergy.objects.filter(user=user)
    serializer = AllergySerializer(allergies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setChildren(request):
    user = request.user
    name = request.data.get('name')
    allergies_data = request.data.get('allergies', [])

    if not name:
        return Response({"detail": "Child name is required."}, status=status.HTTP_400_BAD_REQUEST)

    if allergies_data and not isinstance(allergies_data, list):
        return Response({"detail": "Allergies should be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)

    child = Child.objects.create(name=name, parent=user)

    created_allergies = []
    if allergies_data:
        for allergy_data in allergies_data:
            allergy = Allergy.objects.create(child=child, name=allergy_data['name'])
            allergy_serializer = AllergySerializer(allergy)
            created_allergies.append(allergy_serializer.data)

    child_serializer = ChildSerializer(child)
    response_data = child_serializer.data
    response_data['allergies'] = created_allergies

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteChildren(request, child_id):
    user = request.user

    try:
        child = Child.objects.get(id=child_id, parent=request.user)
    except Child.DoesNotExist:
        return Response({"detail": "Child not found or does not belong to the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

    Allergy.objects.filter(child=child).delete()
    child.delete()

    return Response({"detail": "Child deleted successfully."}, status=status.HTTP_202_ACCEPTED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setChildAllergy(request, child_id):
    try:
        child = Child.objects.get(id=child_id, parent=request.user)
    except Child.DoesNotExist:
        return Response({"detail": "Child not found or does not belong to the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

    new_name = request.data.get('new_name')
    if new_name is not None:
        child.name = new_name
        child.save()  
        
    allergy_names = request.data.get('allergies', [])
    if not isinstance(allergy_names, list):
        return Response({"detail": "Allergies should be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)

    Allergy.objects.filter(child=child).delete()

    created_allergies = []

    for allergy_name in allergy_names:
        allergy = Allergy.objects.create(child=child, name=allergy_name)
        serializer = AllergySerializer(allergy)
        created_allergies.append(serializer.data)

    return Response(created_allergies, status=status.HTTP_200_OK)