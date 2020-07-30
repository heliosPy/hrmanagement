from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from datetime import date
from django.db.models import Q

from .decorator import user_required
from .models import RecuirtmentModel, Applicant
from .forms import (
               ApplicationForm, ApplicantRegistrationForm,
               UserLoginForm, UserRegestrationForm )
from .utils import check_application_date_starts

User = get_user_model()
today = date.today()




def user_login(request):
    """for checking the credentials of the applicant and not the employess"""
    if not request.user.is_anonymous:
        if request.user.is_applicant:
            # if a user is already loged in the they are redirected to the home page
            return redirect('users:home')
    if request.method == "POST":
        logout(request)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_ = form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email_)
            login(request, user)
            return redirect('users:home')
        return render(request, 'applicant/login.html',{'loginform':form})
    form = UserLoginForm()
    return render(request, 'applicant/login.html', {'loginform':form})


def user_register(request):
    if request.method == "POST":
        userre = UserRegestrationForm(request.POST)
        applicant = ApplicantRegistrationForm(request.POST)

        if userre.is_valid() and applicant.is_valid():
            user = userre.save(commit=False)
            user.is_applicant = True
            user.save()
            ali = applicant.save(commit=False)
            ali.user = user
            ali.save()
            return redirect('users:login')
        else:
            return render(request, 'applicant/registration.html',{'user':userre,'applicant':applicant})

    userre = UserRegestrationForm()
    applicant = ApplicantRegistrationForm()
    context = {'user':userre,'applicant':applicant}
    return render(request, 'applicant/registration.html', context)

def user_logout(reqeust):
    logout(reqeust)
    return redirect('home')

@user_required(login_url='/users/login/')
def user_home(request):
    list = RecuirtmentModel.objects.filter(regestration_start__gt=today)
    # to show the list of jobs whose regestration not yet started
    try:
        count = request.user.user_profile.applied.count()
    except:
        count = 0
    return render(request, 'applicant/home.html', {"applied": count,"latest_recu":list})




@user_required(login_url='/users/login/')
def recuir_detail(reqeust, id):
    try:
        data = RecuirtmentModel.objects.get(op_code=id)
    except RecuirtmentModel.DoesNotExist:
        messages.error(reqeust, "The record/recuirtment doesnt exist")
        return redirect('users:home')

    return render(reqeust, 'applicant/detail_rec.html',{'data':data})


def recuir_list(request):
    query=Q(regestration_start__lte=today) & Q(lastdate_apply__gte=today)
    #where jobs which regestration already begain and not over
    q = RecuirtmentModel.objects.filter(query).order_by("-created_on")
    return render(request, 'applicant/Current_Recuriments.html',{"notif": q})

@user_required(login_url='/users/login/')
def apply_application(request,id):
    if  not check_application_date_starts(id):
        messages.error(request, f"The post {id}  which you are trying is doesn't exitst")
        return redirect('users:home')
    cont = request.user.user_profile.mobile
    userr = Applicant.objects.get(mobile=cont)
    post = RecuirtmentModel.objects.get(op_code=id)
    if request.method=='POST':
        application = ApplicationForm(request.POST, request.FILES)
        if application.is_valid():
            app=application.save(commit=False)
            app.post = post
            app.applicant = userr
            app.save()
            messages.success(request, f'You have applied successfully for the job with {id}')
            return redirect('users:home')
        else:
            return render(request, 'applicant/apply.html',{'data':application, 'data1':post})
    try:
        """hear if the user is new the it result in error as the user objects doesnot have applied object"""
        #to check weather the user has already applied to the job so it removes duplicate application
        x=userr.applied.filter(post=id).exists()
        if x:
            message = 'You Have Applied'
            return render(request, 'applicant/apply.html', {"message":message, 'data1': post})
    except:
        pass
    application = ApplicationForm()
    return render(request, 'applicant/apply.html', {'data': application, 'data1':post})



@user_required(login_url='/users/login/')
def applied_list(request):

    try:
        list = request.user.user_profile.applied.all()
        return render(request, 'applicant/apply_list.html',{'data': list})
    except:
        message = "You Have Not Applied for any Jobs"
        return render(request, 'applicant/apply_list.html', {'message': message})

