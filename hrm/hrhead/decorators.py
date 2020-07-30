"""
decorators used in place of login_required
as login_required check on weather a user is authenticated or not
but the hrhead app is accessable only for the hrhead
"""

from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def check_hrhead(u):
    """as the hradmin is a super user it doest have a employee profile,
    if the hradmin user tryin gto access the hrhead app it show DoesNotExist Error"""
    if u.is_authenticated:
        try:
            return u.employee_profile.is_hrhead
        except:
            return False
    else:
        return False


def hrhead_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: check_hrhead(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



