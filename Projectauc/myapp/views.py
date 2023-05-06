from django.contrib.messages.api import success
from django import views
from django.db.models.fields import DateField
from django.http import HttpResponse
from django.core.checks import messages
from django.shortcuts import redirect,render
from django.views import View
from .models import product,Buyer,bidding
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import pytz
from django.utils import timezone
from itertools import chain
from django.conf import settings
from django.core.mail import send_mail

def send_email(name,email):
    subject='Bid Submission'
    message=f'Hello {name},Your bid has been submitted successfully'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
# Create your views here.
utc=pytz.UTC
class product_View(View):
    def get(self,request):
        vehicle=product.objects.filter(category='vehicle',status='onAuction',verified=True)
        realstate=product.objects.filter(category='real state',status='onAuction',verified=True)
        electronics=product.objects.filter(category='electronics',status='onAuction',verified=True)
        sports=product.objects.filter(category='sports',status='onAuction',verified=True)
        jewelry=product.objects.filter(category='jewelry',status='onAuction',verified=True)
        return render(request,'index.html',{'vehicle':vehicle,'realstate':realstate,'electronics':electronics,'sports':sports,'jewelry':jewelry})

class mybiddingView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            myuser = User.objects.get(id=request.user.id)
            newuser=myuser
            myproduct=product.objects.get(pk=pk)
            myprice=myproduct.base_price
            price=myprice+myprice/10
            myobj=bidding.objects.create(current_price=myprice,updated_price=price)
            myobj.save()
            myobj.username.add(myuser)
            myobj.product.add(myproduct)
            myproduct.base_price=price
            myproduct.save()
            myproduct.bids=myproduct.bids+1
            myproduct.save()
            send_email(newuser.first_name,newuser.email)
            return redirect('/')
        else:
            return redirect('login')

class myprofile(View):
    def get(self,request):
        print(request.user.id)
        profile=Buyer.objects.get(pk=request.user.id)
        return render(request,'profile.html',{'profile':profile})


def get_updated(request):
    if request.method=="POST":
        myfile=request.FILES['mydoc']
        profile=Buyer.objects.get(user=request.user)
        profile.profile_img=myfile
        profile.save()
        return redirect('profile')
        
    else:    
        return render(request,'form.html')

class get_details(View):
    def get(self,request):
        myuser=request.user.id
        obj1=bidding.objects.filter(username__id=myuser)
        mypk=[]
        for x in obj1:
            mypk.append(x.pk)
        myobj=bidding.objects.filter(pk__in=mypk)
        myproducts=product.objects.filter(bidding__pk__in=mypk)
        return render(request,'bid-details.html',{'detail':myobj,'result':myproducts})

class listing_page(View):
    def get(self,request):
        query = request.GET.get("query", None)
        products=product.objects.filter(status='onAuction',verified=True)
        if query is not None:
            products = products.filter(title__icontains=query)
        return render(request,'listing.html',{'products':products, 'query':query})

def contact(request):
    return render(request, 'contact.html')

