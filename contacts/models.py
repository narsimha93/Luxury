from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from listings.models import Listing
from django.utils.timezone import now

class Contact(models.Model):
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now)
    user_id = models.IntegerField(blank=True)
    def __str__ (self):
        return self.name
    

class transportation(models.Model):
    listing = models.CharField(max_length=200,blank=True)
    listing_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    owner_phone_number = models.CharField(max_length=100,blank=True)
    onwer_address = models.CharField(max_length=255,blank=True)
    owner_pincode = models.IntegerField(null=True)
    no_of_boxes = models.IntegerField(null=True)
    truck_requirement = models.CharField(max_length=100,blank=True)
    user_id = models.IntegerField(blank=True)
    def __str__(self):
        return self.name
    
class reviews(models.Model):
    #sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    #parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username