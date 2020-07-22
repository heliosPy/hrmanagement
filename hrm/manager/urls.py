#manager app urls
from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns= [
    path('', views.manager_home, name='home'),
    path('login/', views.manager_login, name='login'),
    path('department/' , views.add_department, name='department'),
]