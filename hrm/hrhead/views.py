from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, logout, login
from django.db.models import Q

from hradmin.models import Employee
from manager.models import RecuirtmentModel
from interviewer.models import InterviewSchedule

from .forms import HrheadLoginForm
from .decorators import hrhead_required

User = get_user_model()

today =date.today()
month = today.month

def check_hrhead(user):
    try:
        if user.employee_profile.is_hrhead:
            # "this is  user is already loged in then they are redirected to the home page
            return redirect('hrhead:home')
    except:
        return redirect('home')



def hrhead_login(request):
    """Using the interviewer loginform and inbuilt login method the
        interviwer is loged in"""
    check_hrhead(request.user)
    if request.method == "POST":
        logout(request) #to logout the previous if any
        form = HrheadLoginForm(request.POST)
        if form.is_valid():
            email_ = form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email_)
            login(request, user)
            return redirect('hrhead:home')
        return render(request, 'hrhead/login.html', {'loginform': form})
    form = HrheadLoginForm()
    return render(request, 'hrhead/login.html', {'loginform': form})


@hrhead_required(login_url='/hrhead/login/')
def view_profile(request):
    user = request.user.employee_profile.contact_no
    qs = Employee.objects.get(contact_no=user)
    return render(request, 'hrhead/view_profile.html', {'data': qs})

def logout_hrhead(request):
    logout(request)
    return redirect('home')

@hrhead_required(login_url='/hrhead/login/')
def hrhead_home(request):
    qs = InterviewSchedule.objects.filter(Q(result='Selected') & Q(schedule_date__month=month)).order_by('interview_timestamp')
    return render(request, 'hrhead/home.html', {'selected':qs})

@hrhead_required(login_url='/hrhead/login/')
def recuirtmint_list(request):
    qs = RecuirtmentModel.objects.filter(lastdate_apply__lt=today)
    return render(request,'hrhead/recuirtment_list.html',{'data':qs})

@hrhead_required(login_url='/hrhead/login/')
def rescui_result(request,op):
    rec = get_object_or_404(RecuirtmentModel, op_code=op)
    qs = InterviewSchedule.objects.filter(post=rec)
    qs2 = InterviewSchedule.objects.filter(Q(post=rec) & Q(result='Selected'))
    qs3 = InterviewSchedule.objects.filter(Q(post=rec) & Q(result='Rejected'))
    return render(request, 'hrhead/results.html', {'shortlisted':qs, "selected":qs2, "rejected":qs3,  'rec': rec})

