from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from manager.models import RecuirtmentModel



User = get_user_model()

class Applicant(models.Model):
    name=models.CharField(max_length=30)
    dob = models.DateField()
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    gender= models.CharField(max_length=15)
    qualification = models.CharField(max_length=50, null=True)
    percentage = models.DecimalField(decimal_places=1, max_digits=4, null=True, default=None)
    mobile= models.IntegerField(unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ApplicationFormModel(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applied')
    email = models.EmailField()
    post= models.ForeignKey(RecuirtmentModel,null=True,on_delete=models.SET_NULL, related_name='applicant' )
    resume = models.FileField(upload_to="resumes/")
    applied_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post","applicant"], name='unique application'),
            ]