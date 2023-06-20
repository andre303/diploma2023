from .models import Statistic
from datetime import date
def addLogin():
    if Statistic.objects.filter(date= date.today()).exists():
                    stat = Statistic.objects.get(date= date.today())
                    stat.incLogin()
    else:
        Statistic.objects.create(logins = 1)
def addRegister():
    if Statistic.objects.filter(date= date.today()).exists():
                    stat = Statistic.objects.get(date= date.today())
                    stat.incRegister()
    else:
        Statistic.objects.create(registers = 1)
def addBooking():
    if Statistic.objects.filter(date= date.today()).exists():
                    stat = Statistic.objects.get(date= date.today())
                    stat.incBooking()
    else:
        Statistic.objects.create(bookings = 1)