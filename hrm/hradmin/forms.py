from django import forms
from django.contrib.auth import get_user_model, authenticate

from hradmin.models import Employee


User = get_user_model()


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('user',)

class UserForm(forms.ModelForm):
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

class AdminLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Credentials')
        if not user.is_superuser:
            raise forms.ValidationError('Restricted to Admin only')
        return super().clean()

    def r_user(self):
        return self.user

