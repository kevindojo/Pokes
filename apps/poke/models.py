from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime

# Create your models here.

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


class UserManager(models.Manager):
    def validate_registration(self,post_data):
        errors={}
        for field,value in post_data.iteritems():
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',''))
            if field == "first_name" or field =="last_name" or field == "alias":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',''))
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email']="Invalid Email"
        else:
            if len(self.filter(email=post_data['email']))> 1:
                errors['email']= "Email is already in use"
        if post_data['password'] != post_data['confirmpw']:
            errors['password'] = "Password does not match"
        return errors



    def valid_user(self, post_data):
        hashed = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(5))
        new_user = self.create(
            first_name = post_data['first_name'],
            last_name= post_data['last_name'],
            email = post_data ['email'],
            alias = post_data ['alias'],
            password = hashed
        )
        return new_user
        



    def validate_login(self, post_data):
        errors = {}
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['login']='email/password incorrect'
        else:
            errors['login']='email/password incorrect'
        return errors

    def valid_login(self, post_data):
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
        return user


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)       # needs add
    updated_at = models.DateTimeField(auto_now=True)           # does not need add
    objects = UserManager()
    def __repr__(self):
        return "first:: {} last:: {} ".format(self.first_name,self.last_name)

###########################################################################################################

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poking")
    poked_by = models.ForeignKey(User, related_name="poked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
#This is right, it looks fishy, but trust it!