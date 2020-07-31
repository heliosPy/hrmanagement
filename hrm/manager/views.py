from datetime import date

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, get_user_model,logout
from django.contrib.auth.decorators import  login_required

from .forms import ManagerLoginForm, DepartmentForm, RecuirtmentForm, ScheduleForm
from .models import DepartmentModel, RecuirtmentModel
from .decorators import  manager_required
from hradmin.models import Employee
from interviewer.models import InterviewSchedule
from .utils import check_recu_applic, check_regestration_ends, check_manager



User = get_user_model()

"""////////////////manager user views///////////////////////////////"""
def manager_login(request):
    """Using the managerloginform and inbuilt login method the
        manger is loged in"""
    check_manager(request.user)
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


def check_op_code(request):
    """this is to check the op_code during creating
     new recuirtment weather it exist or not through ajax"""
    if request.is_ajax:
        id = request.GET.get("opid")

        try:
            RecuirtmentModel.objects.get(op_code=id)
            availability = "No"
        except:
            availability = "Yes"
        return HttpResponse(availability)
    #if manauly url is called the it will redirect to the manager home page
    return redirect('manager:home')




@manager_required(login_url='/manager/login/')
def recuirtment_home(request):
    # home page of recuirtment module of manager app
    qs = RecuirtmentModel.objects.all().count()
    return render(request, 'manager/recuirtment.html',{'data':qs})

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


"""////////////////////////////Interview Schedule//////////////////////////////"""
from applicant.models import ApplicationFormModel


today = date.today()

@manager_required(login_url='/manager/login/')
def schedule_home(reqeust):
    rec = RecuirtmentModel.objects.filter(lastdate_apply__lt=today).count()
    appli = ApplicationFormModel.objects.filter(applied_on__date=today).count()
    return render(reqeust, 'manager/schedule.html',{'data':rec,'appli':appli})

@manager_required(login_url='/manager/login/')
def recuirtment_schedle_list(request):
    #list of all recuirtmetn where regestration is completed
    rec = RecuirtmentModel.objects.filter(lastdate_apply__lt=today).order_by("-lastdate_apply")
    return render(request, "manager/recu_schedule_list.html",{'data':rec})




@manager_required(login_url='/manager/login/')
def requirtment_schedule(request,id):
    if not check_regestration_ends(id):
        return redirect('manager:sc_rec_list')
    recuirtmt = RecuirtmentModel.objects.get(op_code=id)
    applicants = ApplicationFormModel.objects.filter(post=recuirtmt)
    return render(request, 'manager/recu_schedule.html',{'rec':recuirtmt, 'appl':applicants})

@manager_required(login_url='/manager/login/')
def schedule_list(request):
    qs = InterviewSchedule.objects.filter(result__exact="Shortlisted")
    return render(request, 'manager/schedule_list.html', {'data':qs})


@manager_required(login_url='/manager/login/')
def ind_schedule(request,id,op):
    if not check_recu_applic(id,op):
        return redirect('manager:sc_rec_list')
    appli = ApplicationFormModel.objects.get(id=id)
    rec = RecuirtmentModel.objects.get(op_code=op)
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.applicant_id = appli
            instance.post = rec
            instance.save()
            return redirect('manager:rec_sched',id=op)
        else:
            return render(request, 'manager/schedule_appli.html',
                          {"data":form, 'applicant':appli, "recuirtment":rec})
    form =ScheduleForm()
    return render(request,'manager/schedule_appli.html',
                  {"data":form,'applicant':appli, "recuirtment":rec})

