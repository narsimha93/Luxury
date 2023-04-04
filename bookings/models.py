from django.db import models
from listings.models import Listing
from django.contrib.auth.models import User
# Create your models here.
PAYMENT_STATUS = (
    ('SUCCESS','SUCCESS'),
    ('FAILURE','FAILURE'),
)
class Bookings(models.Model):
    listing_id = models.ForeignKey(Listing ,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100,blank=True)
    phone_number = models.BigIntegerField(max_length=100,blank=True)
    adhar_card = models.CharField(max_length=100,blank=True)
    pan_card = models.CharField(max_length=100,blank=True)
    family_members = models.CharField(max_length=100,blank=True)
    aggrement = models.FileField(upload_to='aggrement/%Y/%m/%d')
    user_id = models.ForeignKey( User, null=True,on_delete= models.CASCADE,)
    status = models.CharField(choices=PAYMENT_STATUS,null=True,max_length=100)
    #user_id = models.IntegerField( null=True)
    # related to razorpay
    currency = models.CharField(max_length=100, blank=True)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    

    def __str__(self):
        return self.email