from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model

from .models import RecuirtmentModel, Applicant
from .forms import (
               ApplicationForm, ApplicantRegistrationForm,
               UserLoginForm, UserRegestrationForm )

User = get_user_model()





def user_login(request):
    """for checking the credentials of the applicant and not the employess"""
    if not request.user.is_anonymous:
        if request.user.is_applicant:
            # if a user is already loged in the they are redirected to the home page
            return redirect('hradmin:home')
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
    return render(request, 'applicant/login.html',{'loginform':form})


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


def user_home(request):
    q = RecuirtmentModel.objects.all().order_by("-created_on")
    return render(request, 'applicant/home.html', {"notif": q})

