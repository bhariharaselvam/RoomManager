from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class DailyExpenses(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    day = models.DateField()
    user = models.ForeignKey(User)

class MonthlyExpenses(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    day = models.DateField()

class StaticPayments(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()

class MonthlyUserDistribution(models.Model):
    user = models.ForeignKey(User)
    month = models.IntegerField()
    year = models.IntegerField()
    prepaid = models.IntegerField()
    yettopay = models.IntegerField()


