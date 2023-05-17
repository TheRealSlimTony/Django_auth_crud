from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sign_off = models.BooleanField()
    code_review = models.CharField(max_length=50)
    # date_created = models.DateTimeField(auto_now=True)
    # last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
            self.id, self.user, self.sign_off, self.code_review, #self.date_created, self.last_modified
        )
