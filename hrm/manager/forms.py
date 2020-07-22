#this is forms related to manager 
from django import forms
from django.contrib.auth import get_user_model, authenticate

from .models import DepartmentModel, RecuirtmentModel

User = get_user_model()

class ManagerLoginForm(forms.Form):
    """To authenticate weather the user is is_staff  and  only the manger can login"""
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Credentials')
        if not user.is_staff and user.employee_profile.Designation!='Manager':
            raise forms.ValidationError('Restricted to Manager only')
        return super().clean()

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = DepartmentModel
        fields = "__all__"

    def clean_dep_id(self):
        id = self.cleaned_data['dep_id']
        if id <= 100 and id >= 200:
            raise forms.ValidationError('id should be with in range of 100, 200')
        return id

