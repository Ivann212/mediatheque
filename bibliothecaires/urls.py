from django.contrib import admin

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('ajoutmedia/', views.ajoutmedia, name='ajoutmedia'),
    path('deletemedia/<str:nom>/', views.deletemedia, name='deletemedia'),
    path('updatemedia/<str:nom>/', views.updatemedia, name='updatemedia'),
    path('ajoutmembre/', views.ajoutmembre, name='ajoutmembre'),
    path('updatemembre/<int:id>/', views.updatemembre, name='updatemembre'),
    path('deletemembre/<int:id>/', views.deletemembre, name='deletemembre'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
    path('creer_emprunt/', views.creer_emprunt, name='creer_emprunt'),
    path('retourner_media/', views.retourner_media, name='retourner_media'),
    path('listemedias/', views.listemedias, name='listemedias'),
    path('logout/', views.custom_logout, name='logout'),
]
