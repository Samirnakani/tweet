from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=40)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    pic = models.ImageField(upload_to="user/media", blank=True, null=True)

    def __str__(self):
        return self.uname   # ✅ fixed
