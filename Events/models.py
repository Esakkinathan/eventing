from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name=models.CharField('Venue name',max_length=40)
    address=models.CharField(max_length=100)
    zip_code=models.CharField('Zip code',max_length=10)
    phonenumber=models.CharField('Contact phone',max_length=15,blank=True)
    web=models.URLField('website address',blank=True)
    email_address=models.EmailField('Email address',blank=True)
    owner = models.IntegerField("Venue Owner",blank=False ,default=1)
    venue_image = models.ImageField(null=True,blank=True,upload_to="images/")
    
    def __str__(self):
        return  self.name
  
class NewappUser(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email_id=models.EmailField('User email')
    
    
    
    def __str__(self):
        return  self.first_name +' ' +self.last_name    



class Events(models.Model):
    name = models.CharField('Event name',max_length=40)
    event_date=models.DateTimeField('Event date')
    venue=models.ForeignKey(Venue,blank=True,null=True,on_delete=models.CASCADE)
    #venue=models.CharField(max_length=40)
    manager=models.ForeignKey(User,blank=True,null=-True,on_delete=models.SET_NULL)
    description=models.TextField(blank=True)
    attendees=models.ManyToManyField(NewappUser,blank=True)
    approved = models.BooleanField( 'Approved',default=False)
    
    
    def __str__(self):
        return  self.name
    
    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date()-today
        days_till_stripped  = str(days_till).split(",",1)[0]
        return days_till_stripped
    
    @property
    def Is_post(self):
        today = date.today()
        if self.event_date.date() > today:
            thing = "Future"
        else:
            thing = "Past"    
        return thing