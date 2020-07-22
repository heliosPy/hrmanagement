from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_contactno(value):
    if len(str(value)) != 10:
        raise ValidationError("contact no should have 10 digits")



class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ("Manager","Manager"),
        ("HRHead","HRHead"),
        ("Interviwer","Interviwer"),
        ("Employee","Employee"),
    ]
    user = models.OneToOneField(
               settings.AUTH_USER_MODEL,
               on_delete=models.CASCADE,
               primary_key=True,
               related_name='employee_profile')
    name = models.CharField(max_length=50)
    Designation = models.CharField(
               max_length=15,
               choices=DESIGNATION_CHOICES,
               default='Manager')
    contact_no = models.IntegerField(unique=True, validators=[validate_contactno])
    address = models.CharField(max_length=255)



    """for individual authentication based on the designation used on the custom user"""

    @property
    def is_manager(self):
        if self.Designation=='Manager':
            return True
        return False

    @property
    def is_hrhead(self):
        if self.Designation=='HRHead':
            return True
        return False

    @property
    def is_interviwer(self):
        if self.Designation == 'Interviwer':
            return True
        return False

# @receiver(post_save, sender=get_user_model())
# def save_employe_profile(sender, instance, **kwargs):
#     if instance.is_staff:
#         Employee.objects.get_or_create(user=instance)





