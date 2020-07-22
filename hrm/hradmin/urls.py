from django.urls import  path
from hradmin import views


app_name = 'hradmin'

urlpatterns = [
    path('home/', views.hradminhome, name='home'),
    path('login/', views.admin_login, name='login'),
    path('addemp/', views.add_employee, name='addemp'),
    path('allemp/', views.veiw_all_emp, name='allemp'),
    path('update/', views.update_emp, name='update'),
    path('ind_update/', views.ind_update, name='ind_update'),
    path('delemp/', views.del_employe, name='emp_delete'),


]