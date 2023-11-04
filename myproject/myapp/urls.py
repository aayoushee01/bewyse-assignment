from django.urls import path
from . import views

urlpatterns = [
    path('myapp/register/', views.register),
    path('myapp/login/', views.login),
    path('myapp/profile/view/', views.view_profile),
    path('myapp/profile/edit/', views.edit_profile),
]
