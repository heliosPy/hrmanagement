from django.contrib.auth import get_user_model, authenticate
from django import forms

User = get_user_model()

def check_not_hrhead(user):
    try:
        if user.employee_profile.is_hrhead:
            return False
        else:
            return True
    except:
        return True

class HrheadLoginForm(forms.Form):
    """To authenticate weather the user is is_staff  and  only the hrhead can login"""
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Credentials')
        if not user.is_staff or check_not_hrhead(user):
            raise forms.ValidationError('Restricted to Hrhead Only')
        return super().clean()