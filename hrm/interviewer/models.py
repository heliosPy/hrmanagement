from django.db import models



from manager.models import  RecuirtmentModel
from applicant.models import  ApplicationFormModel
from hradmin.models import Employee

class InterviewSchedule(models.Model):
    #to assign a interview from Employee Model who is interviwer and shedule a interviwe
    RESULTS = [
        ("Pending","Pending"),
        ("Shortlisted","Shortlisted"),
        ("Selected","Selected"),
        ("Rejected","Rejected")
    ]
    applicant_id = models.OneToOneField(
                            ApplicationFormModel, primary_key=True,
                            on_delete=models.CASCADE, related_name='interview')
    interviewer_id = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                       limit_choices_to={"Designation": "Interviwer"},
                                       related_name='interviewer')
    schedule_date = models.DateField()
    post = models.ForeignKey(RecuirtmentModel, on_delete=models.CASCADE,
                             related_name='schedule')
    interview_timestamp = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=15, choices=RESULTS, default='Shortlisted')
