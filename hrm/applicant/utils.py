from manager.models import RecuirtmentModel
from datetime import date
from django.db.models import Q


today = date.today()

def check_application_date_starts(x):
    print(x)
    """It return the recuirment which application started """
    query = Q(regestration_start__lte=today) & Q(lastdate_apply__gte=today)
    try:
        RecuirtmentModel.objects.filter(query).get(op_code=x)
    except RecuirtmentModel.DoesNotExist:
        return False
    return True

