from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    pub_date = models.DateTimeField()
    votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)#If user is deleted than delete this product also

    def __str__(self):
        return self.title[:100]

    def summary(self):
        return self.body[:200]
# Create your models here.
