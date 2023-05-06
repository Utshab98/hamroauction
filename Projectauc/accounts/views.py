from django.contrib.messages.api import success
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from myapp.models import Buyer
from django.contrib.auth.models import User,auth
import uuid
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def send_email(name,email,token):
    subject='Verify Your Email'
    message=f'Hello {name},Please click on the link to verify your account  http://localhost:8000/accounts/verify/{token}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
def verify(request,token):
    if Buyer.objects.filter(tokens=token).exists():
        buyer=Buyer.objects.get(tokens=token)
        buyer.verified=True
        messages.success(request,'Now you are verified user,you are Wel-Come')
        buyer.save()
        return redirect('login')
def register(request):
    if request.method=="POST":
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        user_name=request.POST['uname']
        Email=request.POST['mail']
        gender=request.POST['gender']
        country_name=request.POST['country']
        password=request.POST['psw1']
        confirm_pass=request.POST['psw2']
        phone=request.POST['phone']
        file_cat=request.POST['cat']
        myfile=request.FILES['mydoc']
        mydoc=FileSystemStorage()
        file=mydoc.save(myfile.name,myfile)
        file_url=mydoc.url(file)
        address=request.POST['add']
        if password==confirm_pass:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'Username already Exists!')
                return redirect('register')
            elif User.objects.filter(email=Email).exists():
                messages.info(request,'Email already Exists!')
                return redirect('register')
            else:
                uid=uuid.uuid4()
                newuser=User.objects.create_user(username=user_name,password=password,email=Email,first_name=first_name,last_name=last_name)
                newuser.save()
                buyers=Buyer.objects.create(user=newuser,doc_type=file_cat,valid_doc=file_url,contact=phone,address=address,gender=gender,country=country_name,tokens=uid)
                buyers.save()
                send_email(newuser.first_name,newuser.email,uid)
                messages.success(request,"We have sent you a message in your mail,please visit your mail to verify.")
                return redirect('register')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('register')
    
    else:
        return render(request,'register.html')


def login(request):
    if request.method=="POST":
        user_name=request.POST['username']
        password=request.POST['pswd']
        user=auth.authenticate(username=user_name,password=password)
        print(user)
        obj=Buyer.objects.get(user=user)
        if obj.verified:
            auth.login(request,user)
            messages.success(request,"You Logged in Successfully")
            return redirect("/")
        else:
            messages.info(request,'Check the mail and follow the steps to get verified and then try to login')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')