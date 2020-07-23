from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login, get_user_model,logout
from django.contrib.auth.decorators import  login_required

from .forms import ManagerLoginForm, DepartmentForm, RecuirtmentForm
from .models import DepartmentModel, RecuirtmentModel
from .decorators import  manager_required
from hradmin.models import Employee

User = get_user_model()

"""////////////////manager user views///////////////////////////////"""
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
def view_profile(request):
    user = request.user.employee_profile.contact_no
    qs = Employee.objects.get(contact_no=user)
    return render(request, 'manager/view_profile.html', {'data': qs})

def mlogout(request):
    logout(request)
    return redirect('home')

@manager_required(login_url='/manager/login/')
def manager_home(request):
    return render(request, 'manager/home.html')


"""////////////////department related views////////////////////////////////"""

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

@manager_required(login_url='/manager/login/')
def update_ind_department(request):
    id = request.GET.get('id') or request.POST.get('id')
    data = DepartmentModel.objects.get(dep_id=id)
    if request.method == 'POST':
        dep = DepartmentForm(request.POST, instance=data)
        if dep.is_valid() :
            dep.save()
            messages.success(request, "Department Updated Sucessfully")
            return redirect("manager:department")

    qs = DepartmentModel.objects.all()
    form = DepartmentForm()
    return render(request, "manager/ind_update.html",{"depform": form, 'alldep':qs})

@manager_required(login_url='/manager/login/')
def update_delete_department(request):
    qs = DepartmentModel.objects.all()
    return render(request, 'manager/update_department.html',{'alldep':qs})

@manager_required(login_url='/manager/login')
def delete_department(request):
    id = request.GET.get('id')
    data = DepartmentModel.objects.get(dep_id=id).delete()
    return redirect('manager:delupdepartment')



"""///////////////////    Recuirtment views//////////////////////"""

@manager_required(login_url='/manager/login/')
def recuirtment_home(request):
    # home page of recuirtment module of manager app
    qs = RecuirtmentModel.objects.all().count()
    return render(request, 'manager/recuirtment.html')

@manager_required(login_url='/manager/login')
def add_recuirtment(request):
    if request.method == 'POST':
        form = RecuirtmentForm(request.POST)
        if form.is_valid():
            rec=form.save(commit=False)
            print("problem is hera")
            rec.email = request.user.email
            rec.contact = request.user.employee_profile.contact_no
            rec.save()
            return redirect('manager:homerec')
        else:
            return render(request, "manager/add_recuirtment.html",{'data': form })
    form = RecuirtmentForm(request.POST)
    return render(request, "manager/add_recuirtment.html", {'data': form})

@manager_required(login_url='/manager/login/')
def manage_recuirtment(request):
    qs = RecuirtmentModel.objects.all()
    if not qs:
        messages.info(request, 'There is no Recuirtment record')
    return render(request, 'manager/manager_recuirtment.html',{'data':qs})


@manager_required(login_url='/manager/login/')
def update_recuirtment(request):
    id = request.GET.get('id') or request.POST.get('id')
    data = RecuirtmentModel.objects.get(op_code=id)
    if request.method == 'POST':
        form = RecuirtmentForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('manager:homerec')
        else:
            return render(request, 'manager/update_recuirment.html',{'data': form})
    form = RecuirtmentForm(instance=data)
    return render(request, 'manager/update_recuirment.html',{'data': form})



@manager_required(login_url='/manager/login/')
def delete_recuirtment(request):
    if request.method == "POST":
        dlist = request.POST.getlist('t1')
        for i in dlist:
            RecuirtmentModel.objects.get(op_code=i).delete()
        return redirect('manager:homerec')
    qs = RecuirtmentModel.objects.all()
    if not qs:
        messages.info(request, 'There is no Recuirtment record')
    return render(request, 'manager/delete_recuirtment.html', {'data':qs})


