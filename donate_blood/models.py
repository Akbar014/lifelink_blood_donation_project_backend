from django.db import models
from django.contrib.auth.models import User
from . constants import GENDER  , BLOOD_GROUP
# Create your models here.
class UserAccount (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField( upload_to='donate_blood/images/', blank=True, null=True)
    mobile_no = models.CharField(max_length=50)
    age = models.IntegerField( blank=True, null=True)
    blood_group = models.CharField(max_length=50, choices = BLOOD_GROUP,  blank=True, null=True)
    gender = models.CharField(max_length=50, choices = GENDER,  blank=True, null=True)
    address = models.TextField( blank=True, null=True)

    last_donation_date = models.DateField(null=True, blank=True)
    is_available_for_donation = models.BooleanField(default = True)

    def __str__(self):
        return self.user.username
    


class DonationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100,default='patient')
    details = models.TextField()
    location = models.TextField(null= True)
    is_accepted = models.BooleanField(default = False)
    blood_group = models.CharField(max_length=50, choices = BLOOD_GROUP)
    status = models.CharField( max_length=50, default = 'Pending')
    is_completed = models.BooleanField(default = False)
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
    

class DonatioHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE , related_name='donation')
    status = models.CharField( max_length=50) 
    date = models.DateField( auto_now_add=True)


class DonationAccepted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE )
    date = models.DateField( auto_now_add=True)


