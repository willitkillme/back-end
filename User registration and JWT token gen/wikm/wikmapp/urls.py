from django.urls import path # This is the path function
from . import views # This is the views file
from rest_framework_simplejwt.views import TokenRefreshView


# This is the list of our routes
urlpatterns = [
    # Existing routes
    path('', views.getRoutes, name='routes'),

    # Authentication
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
]



