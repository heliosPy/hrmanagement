from django import forms
from django.contrib.auth import get_user_model, authenticate

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

