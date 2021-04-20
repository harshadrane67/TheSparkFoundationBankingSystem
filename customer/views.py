from django.shortcuts import render, redirect
from customer.models import customer, transfer_history
from django.contrib import messages
import re
all_customer_list = customer.objects.all()

def customer_list(request):
    all_customer_list = customer.objects.all().order_by('id')
    return render(request, 'customer.html',{'customer_list':all_customer_list})

def history(request):
    all_transfer_history = transfer_history.objects.all().order_by('-id')
    return render(request,'history.html',{'transfer_history':all_transfer_history})

def profile(request,cust_id):
    sender = customer.objects.get(id=cust_id)
    if request.method == 'POST':
        receiver_id = request.POST['receiver']
        if request.POST['amount_transfer'] == '' or not re.match('[+-]?([0-9]*[.])?[0-9]+', request.POST['amount_transfer']):
            messages.error(request, 'Please Enter Valid amount')
        else:
            amount = float(request.POST['amount_transfer'])

        if receiver_id == 'Select Customer':
            messages.error(request, 'Please Select Customer')
        else:
            receiver = customer.objects.get(id=receiver_id)
            if not amount > sender.balance:
                sender.balance = (sender.balance-amount)
                receiver.balance = (receiver.balance+amount)
                sender.save()
                receiver.save()
                transfer_money = transfer_history(sender=sender,receiver=receiver,amount=amount)
                transfer_money.save()
                messages.success(request, 'Amount Transfered Successfuly')
                
            else:
                messages.error(request, 'Insufficient balance')
            
    return render(request,'profile.html',{'customer_list':all_customer_list, 'sender':sender})

def messages_pages(request):
    return render(request,'message.html')

# Create your views here.
