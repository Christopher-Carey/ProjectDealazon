
from django.db import models
from apps.login_app.models import User

class Product(models.Model):
    url=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    price=models.FloatField()
    users=models.ForeignKey(User, related_name="who_posted")
    img=models.CharField(max_length=255)
    updated_price=models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Deal(models.Model):
    title=models.CharField(max_length=255)
    img=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



