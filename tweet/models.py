from django.db import models
from users.models import User


class Tweet(models.Model):
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tweets/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} by {self.user.uname}"  # from tweet app
