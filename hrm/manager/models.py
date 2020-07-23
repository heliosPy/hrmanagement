from django.db import models
from django.utils import timezone


class DepartmentModel(models.Model):
    dep_id = models.IntegerField(primary_key=True)
    name   = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class RecuirtmentModel(models.Model):
    Experiences_choices = [
        ('Fresher','Fresher'),
        ('One Year', 'One Year'),
        ('Two Years', "Two Years"),
        ("Three Years +","Three Years +"),
        ("Five Years +", "Five Years +"),
        ("Ten Years +","Ten Years +" ),
        ("Not Required", "Not Required")
    ]

    op_code            = models.IntegerField(primary_key=True)
    qualification      = models.CharField(max_length=255)
    regestration_start = models.DateField()
    experience         = models.CharField(max_length=15, choices=Experiences_choices, default='Fresher')
    lastdate_apply     = models.DateField()
    department         = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE)
    no_positions       = models.IntegerField()
    description        = models.TextField()
    responsibilites    = models.CharField(max_length=200)
    contact            = models.IntegerField()
    email              = models.EmailField()
    created_on =         models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description