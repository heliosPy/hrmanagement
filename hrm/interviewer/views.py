from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout, login

from hradmin.models import Employee
from .models import InterviewSchedule
from .forms import InterviewerLoginForm, InterviewForm
from .decorator import interviewer_required

User = get_user_model()
today = date.today()

def check_interviewer(user):
    try:
        if user.employee_profile.is_interviwer:
            # "this is  user is already loged in then they are redirected to the home page
            return redirect('interviewer:home')
    except:
        return redirect('home')

def interviewer_login(request):
    """Using the interviewer loginform and inbuilt login method the
        interviwer is loged in"""
    check_interviewer(request.user)
    if request.method == "POST":
        logout(request) #to logout the previous if any
        form = InterviewerLoginForm(request.POST)
        if form.is_valid():
            email_ = form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email_)
            login(request, user)
            return redirect('interviewer:home')
        return render(request, 'interviewer/login.html', {'loginform': form})
    form = InterviewerLoginForm()
    return render(request, 'interviewer/login.html', {'loginform': form})


@interviewer_required(login_url='/interviewer/login/')
def view_profile(request):
    user = request.user.employee_profile.contact_no
    qs = Employee.objects.get(contact_no=user)
    return render(request, 'interviewer/view_profile.html', {'data': qs})

def logout_interv(request):
    logout(request)
    return redirect('home')

@interviewer_required(login_url='/interviewer/login/')
def interviewer_home(request):
    try:
        count = request.user.employee_profile.interviewer.filter(schedule_date__exact=today).count()
    except:
        count = 0
    return render(request, 'interviewer/home.html',{'count':count})


@interviewer_required(login_url='/interviewer/login/')
def today_interviews(request):
    try:
        qs = request.user.employee_profile.interviewer.filter(schedule_date__exact=today)
    except:
        qs = []
    print(qs)
    return render(request, 'interviewer/today_interviews.html',{"data":qs})

@interviewer_required(login_url='/interviewer/login/')
def interview(request,id):
    data = InterviewSchedule.objects.get(applicant_id_id=id)
    if data.result != 'Shortlisted':
        message = "Interview Completed"
        return render(request, "interviewer/interview.html", {"data":data,'message':message})
    if request.method == "POST":
        form = InterviewForm(request.POST, instance=data)
        if form.is_valid():
            x = form.save(commit=False)
            x.interview_timestamp = datetime.now()
            x.save()
            return redirect('interviewer:today_list')
        else:
            return render(request, 'interviewer/interview.html', {'form':form, "data":data})
    form = InterviewForm(instance=data)
    return render(request, 'interviewer/interview.html', {'form': form, "data": data})





