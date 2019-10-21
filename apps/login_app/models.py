from django.db import models
import re

class UserManager(models.Manager):
    def basic_validation(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = ("Invalid email address!")
        if len(postData["first_name"]) < 2:
            errors["first_name"]="-At least 2 characters-"
        if len(postData["last_name"]) < 2:
            errors["last_name"]="-At least 2 characters-"
        if postData["password"] != postData["pwconfirm"]:
            errors["pwmatch"]="-PW do not match-"
        if len(postData["password"]) < 8:
            errors["password"]="-At least 8 characters-"

        

        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()