from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('profile/<str:login>', views.profile)
]
