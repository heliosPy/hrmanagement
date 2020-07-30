from datetime import date

from django.shortcuts import redirect

from .models import RecuirtmentModel
from applicant.models import ApplicationFormModel


today = date.today()

def check_regestration_ends(x):
    """To check the id got from url
    weather the object exist and if
    exits its regestration should end"""
    try:
        if RecuirtmentModel.objects.filter(lastdate_apply__lt=today).get(op_code=x):
            return True
        else:
            return False
    except RecuirtmentModel.DoesNotExist:
        return False

def check_recu_applic(x, y):
    """to check the applicant and recuirtmetn model exist or not
    """
    try:
        RecuirtmentModel.objects.get(op_code=y)
        ApplicationFormModel.objects.get(id=x)
    except:
        return False
    return True

def check_manager(user):
    try:
        if user.employee_profile.is_manager:
            # "this is  user is already loged in then they are redirected to the home page
            return redirect('manager:home')
    except:
        return redirect('home')