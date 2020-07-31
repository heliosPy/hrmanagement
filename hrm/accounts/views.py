from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def homeview(request):
    return render(request, 'new body.html')

def usr_logout(request):
    user = request.user
    if user:
        logout(request)
        messages.success(request, "successfully logout")
        return redirect('home')
    return redirect('home')