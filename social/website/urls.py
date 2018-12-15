from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.sign_up),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('post', views.post),
    path('tag/<str:tag>', views.tags),
    path('profile/<str:login>', views.profile),
    path('follow/', views.follow),
    path('thumb-give/', views.thumb_give)
]
