from django.db import models
from django.contrib.auth import get_user_model
from manager.models import RecuirtmentModel



User = get_user_model()

class Applicant(models.Model):
    name=models.CharField(max_length=30)
    dob = models.DateField()
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    gender= models.CharField(max_length=15)
    mobile= models.IntegerField(unique=True)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class ApplicationFormModel(models.Model):
    name = models.CharField(max_length=30)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applied')
    dob = models.DateField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=15)
    mobile = models.IntegerField(unique=True)
    address = models.CharField(max_length=150)
    qualification= models.CharField(max_length=50)
    percentage = models.DecimalField(decimal_places=1, max_digits=4)
    post= models.ForeignKey(RecuirtmentModel,null=True,on_delete=models.SET_NULL )
    resume = models.FileField(upload_to="resumes/")

    def __str__(self):
        return self.name