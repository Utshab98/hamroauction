from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.core.mail import send_mail
from django.conf import settings
#Create your models here.
# def send_email(name,email,token):
#     subject='Bid Submission'
#     message=f'Hello {name},Your bid has been submitted successfully'
#     from_email=settings.EMAIL_HOST_USER
#     recipient_list=[email]
    #send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
CAT_choices=(
    ('jewelry','jewelry'),
    ('vehicle','vehicle'),
    ('sports','sports'),
    ('real state','real state'),
    ('electronics','electronics'),
    ('others','others'),
)
STAT_choices=(
    ('notSpecified','not specified'),
    ('onAuction','on auction'),
    ('sold','sold'),
    ('unsold','unsold'),
)

doc_choice=(
    ('citizenship','citizenship'),
    ('Driving-License','Driving-License'),
    ('Passport','Passport')
)
gender_cat=(
    ('male','male'),
    ('female','female')
)
class product(models.Model):
    pro_id=models.PositiveIntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    img=models.ImageField(upload_to='products')
    base_price=models.FloatField()
    category=models.CharField(max_length=30,choices=CAT_choices)
    status=models.CharField(choices=STAT_choices,max_length=25)
    verified=models.BooleanField(default=False)
    auction_start=models.DateTimeField()
    auction_expiration=DateTimeField()
    bids=models.PositiveIntegerField(default=0)

    class Meta:
        ordering=['pro_id']
    

class bidding(models.Model):
    current_price=models.FloatField()
    bid_date=models.DateTimeField(auto_now_add=True)
    updated_price=models.FloatField()
    product=models.ManyToManyField(product)
    username=models.ManyToManyField(User)
    
class Buyer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_img=models.ImageField(upload_to='mydoc',default="profile.png")
    doc_type=models.CharField(max_length=30,choices=doc_choice)
    valid_doc=models.ImageField(upload_to='verified_doc')
    contact=models.CharField(max_length=12)
    address=models.CharField(max_length=60)
    verified=models.BooleanField(default=False)
    country=models.CharField(max_length=35)
    gender=models.CharField(max_length=10,choices=gender_cat)
    tokens=models.CharField(max_length=150,null=True)
    