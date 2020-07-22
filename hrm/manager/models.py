from django.db import models



class DepartmentModel(models.Model):
    dep_id = models.IntegerField(primary_key=True)
    name   = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class RecuirtmentModel(models.Model):
    op_code            = models.IntegerField(primary_key=True)
    qualification      = models.CharField(max_length=15)
    regestration_start = models.DateField()
    age_limit          = models.IntegerField()
    lastdate_apply     = models.DateField()
    department         = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE)
    no_positions       = models.IntegerField()
    description        = models.TextField()
    responsibilites    = models.CharField(max_length=200)
    contact            = models.IntegerField()
    email              = models.EmailField()

    def __str__(self):
        return self.responsibilites