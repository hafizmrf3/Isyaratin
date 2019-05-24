from django.contrib.auth.models import Permission, User
from django.db import models
# Create your models here.

class SignLanguage(models.Model):

    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT )
    name = models.CharField(max_length=40)
    website = models.CharField(max_length=40)
    logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name + '-' + self.website


class Huruf(models.Model):

    signlanguage = models.ForeignKey(SignLanguage, on_delete=models.CASCADE)
    huruf = models.CharField(max_length=50)
    cover = models.FileField(default='')
   
    def __str__(self):
        return self.huruf