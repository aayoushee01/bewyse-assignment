from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register),
    path('accounts/login/', views.login),
    path('accounts/profile/view/', views.view_profile),
    path('accounts/profile/edit/', views.edit_profile),
]
