from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

# Create your models here.

class UserModel(AbstractUser):
    username = None
    password = models.CharField(max_length=128,blank=True,null=True)
    google = models.BooleanField(default=False)
    sub = models.TextField(blank=True,null=True)
    picture_url = models.URLField(null=True,blank=True)
    google_picture = models.URLField(null=True,blank=True)                                              
    email = models.EmailField(_("Email"),unique=True,max_length=50)
    mobile_number = models.CharField(_("Mobile number"),max_length=20,blank=True)
    first_name = models.CharField(_("First Name"),max_length=20,blank=True)
    last_name = models.CharField(_("Last name"),max_length=20,blank=True)
    image = models.URLField(blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if self.password == None:  
            self.google = True
        if self.password:
           self.password = make_password(self.password)
        super().save(*args,**kwargs)



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # objects = UserManager()

    def __str__(self):
        return self.email
    
