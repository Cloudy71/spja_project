from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signin', views.sign_in),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('profile/<str:login>', views.profile)
]
