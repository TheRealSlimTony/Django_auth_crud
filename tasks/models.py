from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=201)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.title, self.user)


class Snippet(models.Model):
    title = models.CharField(max_length=201)
    descripcion = models.TextField(blank=True)
    language = models.CharField(max_length=50, default="Python")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_gpt_explanation = models.TextField(blank=True)
    public_snippet = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
            self.id, self.title, self.user, self.language, self.public_snippet
        )
