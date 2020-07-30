"""
decorators used in place of login_required
as login_required check on weather a user is authenticated or not
but the applicant app is accessable only for the applicants ie users
"""

from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def check_user(u):
    if u.is_authenticated:
        return u.is_applicant
    else:
        return False




def user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: check_user(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



