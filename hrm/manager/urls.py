#manager app urls
from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns= [
    path('', views.manager_home, name='home'),
    path('login/', views.manager_login, name='login'),
    path('profile/', views.view_profile, name='profile'),
    path('logout/', views.mlogout, name='logout'),

    #department urls
    path('department/' , views.add_department, name='department'),
    path('delupdep/', views.update_delete_department, name='delupdepartment'),
    path('updatedep/', views.update_ind_department, name='updatedep'),
    path('deldepartment/', views.delete_department, name='delete_department'),

    # recuitment urls
    path('recuitment/',views.recuirtment_home, name='homerec'),
    path('addrec/', views.add_recuirtment, name='addrec'),
    path('managerec/', views.manage_recuirtment, name ='manarec'),
    path('updaterec/', views.update_recuirtment, name='updaterec'),
    path('deleterec/', views.delete_recuirtment, name='deleterec'),

    #interviwe schedule
    path('schedule/', views.schedule_home, name='schedule'),
    path('schedule/reqlist/', views.recuirtment_schedle_list, name='sc_rec_list'),
    path('schedule/reqlist/sud/<int:id>', views.requirtment_schedule, name="rec_sched"),
    path('schedule/ind/<int:id>/<int:op>/', views.ind_schedule, name='app_sched'),
    path('schedule/list/', views.schedule_list, name='schedule_list'),

    #Ajax
    path('check/', views.check_op_code, name="check"),
]