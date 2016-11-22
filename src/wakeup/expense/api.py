from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.contrib.auth import get_user_model
from django.db.models import Sum
import datetime

d = datetime.date.today()
month = d.month
year = d.year







class ExpenseView(ViewSet):
    base_url = r'/expense'
    base_name = ''

    def create(self, request):
        if not request.user.is_authenticated():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data
            name = data['name'] if 'name' in data.keys() else ""
            amount = data['amount'] if 'amount' in data.keys() else 0
            date = data['date'] if 'date' in data.keys() else None
            result = True
            try:
                DailyExpenses.objects.create(user=request.user, name=name, amount=amount,day=date)
            except Exception as e:
                print str(e)
                result = False

            if result:
                return Response({"result": "Amount added", "status": True})
            else:
                return Response({"result": "Failed to add amount", "status": False})
        except Exception as e:
            print str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            sort = request.GET.get('sort', "day")
            order = request.GET.get('order', None)
            result = []

            if order=="desc":
                sort="-"+sort
            for obj in DailyExpenses.objects.all().filter(day__month=month,day__year=year).order_by(sort):
                result.append({"id":obj.id,"date":obj.day,"amount":obj.amount,"description":obj.name,"user":obj.user.username})
            return Response(result)

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = DailyExpenses.objects.get(id=pk)
        return Response({"id":obj.id,"date":obj.day,"amount":obj.amount,"description":obj.name,"user":obj.user.username})



class EditableView(ViewSet):
    base_url = r'/editable'
    base_name = ''


    def create(self, request):
        if not request.user.is_authenticated():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data
            name = data['name'] if 'name' in data.keys() else ""
            amount = data['amount'] if 'amount' in data.keys() else 0
            date = data['date'] if 'date' in data.keys() else None
            result = True
            try:
                DailyExpenses.objects.create(user=request.user, name=name, amount=amount,day=date)
            except Exception as e:
                print str(e)
                result = False

            if result:
                return Response({"result": "Amount added", "status": True})
            else:
                return Response({"result": "Failed to add amount", "status": False})
        except Exception as e:
            print str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            result = []
            for obj in DailyExpenses.objects.all().filter(user=request.user,day__month=month,day__year=year):
                result.append({"id":obj.id,"date":obj.day,"amount":obj.amount,"description":obj.name,"user":obj.user.username})
            return Response(result)

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            obj = DailyExpenses.objects.get(id=pk)
            return Response({"id":obj.id,"date":obj.day,"amount":obj.amount,"description":obj.name,"user":obj.user.username})
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            expense = DailyExpenses.objects.filter(id=pk)[0]
            if expense.user == request.user:
                expense.delete()
                return Response({"result": "Amount removed successfully", "status": True})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"result": "Amount was not removed", "status": False})

    @csrf_exempt
    def partial_update(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:

            data = request.data
            name = data['name'] if 'name' in data.keys() else ""
            amount = data['amount'] if 'amount' in data.keys() else 0
            date = data['date'] if 'date' in data.keys() else None
            obj = DailyExpenses.objects.get(id=pk)
            edit = 0
            if amount != 0 and obj.user == request.user:
                obj.amount = amount
                edit = 1
            if name != "" and obj.user == request.user:
                obj.name = name
                edit = 1
            if date != None and obj.user == request.user:
                obj.date = date
                edit =1
            if edit ==1:
                obj.save()
                return Response({"result": "Amount edited", "status": True})
            else:
                return Response({"result": "Failed to edit amount", "status": False})
        except Exception as e:
            print str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AggregateUser(ViewSet):
    base_url = r'/useramount'
    base_name = ''

    def create(self, request):
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            User = get_user_model()
            result = []
            for user in User.objects.all():
                agg=DailyExpenses.objects.filter(user=user,day__month=month,day__year=year).aggregate(Sum('amount'))
                #print count['amount__sum']
                count = agg['amount__sum'] if agg['amount__sum'] else 0
                result.append({"name":user.username,"y":count})
            return Response(result)

    def retrieve(self, request, code=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PaymentView(ViewSet):
    base_url = r'/payment'
    base_name = ''

    def create(self, request):
        if not request.user.is_authenticated():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data
            name = data['name'] if 'name' in data.keys() else ""
            amount = data['amount'] if 'amount' in data.keys() else 0
            result = True
            try:
                StaticPayments.objects.create(name=name, amount=amount)
            except Exception as e:
                print str(e)
                result = False

            if result:
                return Response({"result": "Payment added", "status": True})
            else:
                return Response({"result": "Failed to add payment", "status": False})
        except Exception as e:
            print str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            result = []
            for obj in StaticPayments.objects.all():
                result.append({"id":obj.id,"amount":obj.amount,"description":obj.name})
            return Response(result)

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = StaticPayments.objects.get(id=pk)
        return Response({"id":obj.id,"amount":obj.amount,"description":obj.name})

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            expense = StaticPayments.objects.filter(id=pk)[0]
            expense.delete()
            return Response({"result": "Amount removed successfully", "status": True})
        except Exception as e:
            print str(e)
            return Response({"result": "Amount was not removed", "status": False})

    @csrf_exempt
    def partial_update(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:

            data = request.data
            name = data['name'] if 'name' in data.keys() else ""
            amount = data['amount'] if 'amount' in data.keys() else 0

            obj = StaticPayments.objects.get(id=pk)
            if amount != 0 :
                obj.amount = amount
            if name != "" :
                obj.name = name
            if amount != 0 or name != None:
                obj.save()
                return Response({"result": "Amount edited", "status": True})
            else:
                return Response({"result": "Failed to edit amount", "status": False})
        except Exception as e:
            print str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



