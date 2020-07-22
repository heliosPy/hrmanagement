from django.shortcuts import render,redirect
from django.contrib.auth import login, get_user_model,logout
from django.contrib.auth.decorators import  login_required

from .forms import ManagerLoginForm, DepartmentForm
from .models import DepartmentModel, RecuirtmentModel
from .decorators import  manager_required

User = get_user_model()


def manager_login(request):
    """Using the managerloginform and inbuilt login method the
        manger is loged in"""
    if not request.user.is_anonymous and not request.user.is_superuser:
        if request.user.is_superuser:
            #"this is  user is already loged in then they are redirected to the home page
            return redirect('manager:home')
    if request.method == "POST":
        logout(request) #to logout the previous if any
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            email_ = form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email_)
            login(request, user)
            return redirect('manager:home')
        return render(request, 'manager/login.html', {'loginform': form})
    form = ManagerLoginForm()
    return render(request, 'manager/login.html', {'loginform': form})


@manager_required(login_url='/manager/login/')
def manager_home(request):
    return render(request, 'manager/home.html')

@manager_required(login_url='/manager/login/')
def add_department(request):
    """ Adding the departments to the data base using department model """
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('manager:department')
    qs = DepartmentModel.objects.all()
    form = DepartmentForm()
    return render(request, 'manager/department.html',{'depform':form, 'alldep':qs})
