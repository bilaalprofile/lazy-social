from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="profiles/")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="posts/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
