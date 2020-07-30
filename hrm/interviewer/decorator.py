"""
decorators used in place of login_required
as login_required check on weather a user is authenticated or not
but the intervieweer app is accessable only for the interviwer
"""

from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def check_interviewer(u):
    """as the hradmin is a super user it doest have a employee profile,
    if the hradmin user tryin gto access the manager app it show DoesNotExist Error"""
    if u.is_authenticated:
        try:
            return u.employee_profile.is_interviwer
        except:
            return False
    else:
        return False


def interviewer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: check_interviewer(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



