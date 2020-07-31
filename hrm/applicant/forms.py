from django import forms
from django.contrib.auth import get_user_model, authenticate
import re

from .models import Applicant, ApplicationFormModel


class ApplicantRegistrationForm(forms.ModelForm):
    gen = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    gender = forms.ChoiceField(choices=gen, widget=forms.RadioSelect)
    class Meta:
        model = Applicant
        exclude = ('user',)


    def clean_name(self):
        name=self.cleaned_data["name"]
        re_name=re.findall(r'^[a-zA-Z.]*$',name)
        if re_name:
            return name
        else:
            raise forms.ValidationError("The name Should Contain Alphabits only")

    def clean_mobile(self):
        no = self.cleaned_data['mobile']
        if len(str(no))!=10:
            raise forms.ValidationError('Mobile Number should contain 10 digits')
        return no

class UserRegestrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


    def clean_password(self):
        password=self.cleaned_data["password"]
        repass =re.findall(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%.])[a-zA-Z0-9@#$%.]{8,}$',password)
        # this is regular expression for atleast one small& big letters, one numerical, one special character and then the total length is min 8characters
        if repass:
            # "The Password Should Contain atleast 8 characters with min one lowercase,one uppercase, one digit and  one special characters '@#$%.'"
            return password
        else:
            raise forms.ValidationError(" min 8 char with atleast 1 (Upper, lower, numeric and @#$%. character ")



    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("passwords are not matching")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Credentials')
        if not user.is_applicant:
            raise forms.ValidationError('Restricted to Applicants only')
        return super().clean()

class ApplicationForm(forms.ModelForm):
    class Meta:
        model=ApplicationFormModel
        fields = ("email",'resume')

