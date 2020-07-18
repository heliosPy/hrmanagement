#forms.py for overriding the default user forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreation(UserCreationForm):

    class meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChange(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
