#this is forms related to manager 
from django import forms
from django.contrib.auth import get_user_model, authenticate

from .models import DepartmentModel, RecuirtmentModel

User = get_user_model()

def check_not_manager(user):
    try:
        if user.employee_profile.is_manager:
            return False
        else:
            return True
    except:
        return True

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
        if not user.is_staff or check_not_manager(user):
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

class RecuirtmentForm(forms.ModelForm):
    class Meta:
        model = RecuirtmentModel
        exclude = ("contact", "email","created_on")

    def clean_op_code(self):
        id = self.cleaned_data['op_code']
        if id <= 1000:
            raise forms.ValidationError("oppertunity code should be greater than 1000")
        return id



from interviewer.models import  InterviewSchedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        exclude = ('post','applicant_id','interview_timestamp', 'result')
