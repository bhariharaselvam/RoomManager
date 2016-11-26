import datetime
from django.db.models import Sum
from .models import *
d = datetime.date.today()
month = d.month

def get_users(month,year):
    return DailyExpenses.objects.all().filter(day__month=month,day__year=year).values_list('user').distinct()

def user_expense(month,year,user):
    return DailyExpenses.objects.all().filter(day__month=month,day__year=year,user=user).aggregate(Sum('amount'))

def calculate(month,year):
    users = get_users(month,year)
    for user in users:
        if len(MonthlyUserDistribution.objects.all().filte(day__month=month,day__year=year,user=user))==0:
            MonthlyUserDistribution.objects.create(month=month,year=year,user=user)

    for user in users:
        obj = MonthlyUserDistribution.objects.all().filte(day__month=month,day__year=year,user=user)[0];
        obj.prepaid = user_expense(month,year,user)
        obj.save()
    return True




