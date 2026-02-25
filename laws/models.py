from django.db import models

class Law(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    law = models.ForeignKey(Law, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.law.title}"