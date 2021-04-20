from django.shortcuts import render
from customer.models import customer

def home(request):
    customer_list = customer.objects.all()
    return render(request,'index.html',{'customer_list':customer_list})


# Create your views here.
