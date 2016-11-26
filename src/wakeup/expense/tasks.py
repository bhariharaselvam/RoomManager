import datetime
from django.db.models import Sum
from django.contrib.auth import get_user_model
from .models import *
d = datetime.date.today()
month = d.month

def get_users(month,year):
    return DailyExpenses.objects.all().filter(day__month=month,day__year=year).values_list('user').distinct()

def user_expense(month,year,user):
    return DailyExpenses.objects.all().filter(day__month=month,day__year=year,user=user).aggregate(Sum('amount'))

def calculate(month,year):
    users = get_users(month,year)
    User = get_user_model()

    #create user rows
    for user in users:
        user_obj=User.objects.get(id=user[0])
        print user_obj
        if len(MonthlyUserDistribution.objects.all().filter(month=month,year=year,user=user_obj))==0:
            MonthlyUserDistribution.objects.create(month=month,year=year,user=user_obj,prepaid=0,yettopay=0)
    total_static_payments = StaticPayments.objects.all().aggregate(Sum('amount'))
    print total_static_payments
    total_user_payements = DailyExpenses.objects.all().filter(day__month=month,day__year=year).aggregate(Sum('amount'))
    print total_user_payements
    total_payments = total_static_payments['amount__sum'] + total_user_payements['amount__sum']
    print total_payments
    average = total_payments / len(users)
    print average

    for user in users:
        user_obj=User.objects.get(id=user[0])
        prepaid = user_expense(month,year,user_obj)
        prepaid = prepaid['amount__sum']
        obj = MonthlyUserDistribution.objects.all().filter(month=month,year=year,user=user_obj)[0]
        obj.prepaid = prepaid
        obj.yettopay = average - prepaid
        obj.save()
    for sp in MonthlyBudget.objects.all().filter(month=month,year=year):
        sp.delete()
    for sp in StaticPayments.objects.all():
        MonthlyBudget.objects.create(month=month,year=year,name=sp.name,amount=sp.amount)
    MonthlyBudget.objects.create(month=month,year=year,name="total_static_payments",amount=total_static_payments['amount__sum'])
    MonthlyBudget.objects.create(month=month,year=year,name="total_user_payments",amount=total_user_payements['amount__sum'])
    MonthlyBudget.objects.create(month=month,year=year,name="total_payments",amount=total_payments)
    MonthlyBudget.objects.create(month=month,year=year,name="average_to_users",amount=average)

    return True






