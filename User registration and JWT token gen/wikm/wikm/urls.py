"""
URL configuration for wikm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from wikmapp import views
from wikmapp.views import RegisterView
from wikmapp.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.home, name='home'),  # Define the root URL pattern and point it to the 'home' view function (Not sure if it is necessary)
    path('api/register/', RegisterView.as_view(), name='register'),
    path("admin/", admin.site.urls),
    path('wikmapp/', include('wikmapp.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/profile/', views.getProfile, name='profile'),
]
