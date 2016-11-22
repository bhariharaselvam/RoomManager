import datetime
from django.db.models import Sum
from .models import *
d = datetime.date.today()
month = d.month

def cal_total():
    return DailyExpenses.objects.all().filter(day__month_lte=month).aggregate(Sum('amount'))



