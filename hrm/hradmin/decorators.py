"""
decorators used in place of login_required
as login_required check on weather a user is authenticated or not
but the hradmin is accessable only for the superuser
"""
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import   user_passes_test

def hradmin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):

    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator