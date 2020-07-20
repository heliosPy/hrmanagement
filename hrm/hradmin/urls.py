from django.urls import  path
from hradmin import views

urlpatterns = [
    path('', views.createemployee, name = 'home')
]