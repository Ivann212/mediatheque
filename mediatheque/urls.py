from tkinter.font import names

from django.contrib import admin

from django.urls import path
from bibliothecaires import views
from django.contrib.auth import views as auth_views

from django.urls import path, include
from bibliothecaires import views as bibliothecaires_views


urlpatterns = [
    path('', views.listemedias, name='listemedias'),
    path('bibliothecaires/', include('bibliothecaires.urls')),
    path('admin/', admin.site.urls),
]
