from django.shortcuts import render , HttpResponse , redirect
from .forms import AccountForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
# Create your views here.
def home(request):
    return render(request,"index.html")
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Account

def create(request):
    form = AccountForm()
    if request.method =="POST":
        form = AccountForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print("successfull")
            # print(form.data)
            reciver_email = form.data["email"]
            data = Account.objects.get(email =reciver_email )
            acc = data.account_number
            try:
                send_mail(
                    "Thanks for Registration",   # subject
                    f"Thank you for registering with our proBank. We are excited to have you on board! your account number is {acc} ,\n thank you \n regards \n ProBank manager  ", # body 
                    settings.EMAIL_HOST_USER,  
                    [reciver_email],  
                    fail_silently=False,
                )
                print("mail sent")
                return  redirect("home")
            except Exception as e:
                return HttpResponse(f"Error sending email: {e}")

    return render(request,"create.html",{'form':form})

    
def pin(request):
    if request.method =="POST":
        acc = request.POST.get("acc")
        mobile = request.POST.get("phone")
        pin = int(request.POST.get("pin"))
        cpin =int(request.POST.get("cpin"))
        print(acc,mobile,pin,cpin)
        try:

            account = Account.objects.get(account_number = acc)
        except :
            return HttpResponse("account  not found in database ")
        finally:
            print("exception is handled")
        if account.mobile == int(mobile):
            
            if pin  == cpin:
                pin += 111
                
                account.pin = pin
                account.save()

                print("pin added")
            else:
                print("both pins dont match")
    return render(request,'pin.html')

def balance(request):
    balance = 0
    var=False
    if request.method == "POST":
        var=True
        acc = request.POST.get("acc")
        pin=int(request.POST.get("pin"))
        print(acc,pin)
        try:
            account = Account.objects.get(account_number = acc)
            print(account)
        except :
            return HttpResponse("account  not found in database ")
        encpion = account.pin-111
        if pin==encpion:
            print("pin matched")
            balance = account.balance
            print(balance)
            subject = "Balance Enquiry"
            message = f"Your account balance is {balance}"
            reciver_email = account.email
            send_mail(
                    'dear vicky', 
                    'your money was deposit',
                    settings.EMAIL_HOST_USER,  
                    [reciver_email],  
                    fail_silently=False,
                )
            print("mail sent")
        else:
            return HttpResponse("pin not matched")
    return render(request,'balance.html',{'balance':balance,'var':var})


def deposit(request):
    if request.method == "POST":
        acc = request.POST.get("acc")
        mobile = request.POST.get("mobile")
        amount = int(request.POST.get("amount"))
        print(acc,mobile,amount)
        try:
            account = Account.objects.get(account_number = acc)
        except :
            return HttpResponse("account  not found in database ")
        finally:
            print("exception is handled")
        if account.mobile == int(mobile):
            print('account verified')
            if amount>=100 and amount<=10000:
                account.balance += int(amount)
                account.save()
            else:
                return HttpResponse("amount should be between 100 and 10000")
            print("amount added")
        else:
            print("both mobiles dont match")
        
    return render(request,'deposit.html')

def withdraw(request):
    if request.method == "POST":
        acc = request.POST.get("acc")
        pin=request.POST.get("pin")
        amount = int(request.POST.get("amount"))
        print(acc,pin,amount)
        try:
            account = Account.objects.get(account_number = acc)
        except :
            return HttpResponse("account  not found in database ")
        finally:
            print("exception is handled")
        pin=account.pin-111    
        if account.pin == int(pin):
            print('account verified')
            if amount>=100 and amount<=account.balance:
                account.balance -= int(amount)
                account.save()
            else:
                return HttpResponse("amount should be between 100 and balance")
            print("amount added")
        else:
            print("both pins dont match")
    return render(request,'withdraw.html')

def transfer(request):
    if request.method == "POST":
        fromAcc = request.POST.get("fromAcc")
        toAcc = request.POST.get("toAcc")
        amount = int(request.POST.get("amount"))
        pin = int(request.POST.get("pin"))
        print(fromAcc,toAcc,amount)
        try:
            fromAccount = Account.objects.get(account_number = fromAcc)
        except :
            return HttpResponse("from account not found in database ")
        try:
            toAccount = Account.objects.get(account_number = toAcc)
        except :
            return HttpResponse("to account not found in database ")
        frompin = fromAccount.pin - 111
        if frompin == pin:
            if amount>=100 and amount<=fromAccount.balance:
                fromAccount.balance -= int(amount)
                toAccount.balance += int(amount)
                fromAccount.save()
                toAccount.save()
            else:
                return HttpResponse("amount should be between 100 and balance")
        else:
            return HttpResponse("pin not matched")
    return render(request,'transfer.html')
