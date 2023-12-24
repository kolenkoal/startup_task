from django.db import models

from users.models import User


class Link(models.Model):
    id = models.CharField(max_length=8, unique=True, primary_key=True)
    last_accessed = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.id
