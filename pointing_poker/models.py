from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class GameSession(models.Model):
    name = models.CharField(max_length=200, default='New Game Session')
    description = models.CharField(max_length=200, default='test')
    start_time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return '{} - {} {}'.format(self.name,self.description,self.start_time)
    

class Card(models.Model):
    name = models.CharField(max_length=200)
    value = models.IntegerField()

    def __str__(self):
        return '{} - {} {}'.format(self.name,self.value)
    

class vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete= models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} voted for {self.card} in {self.game_session}"


class Participant(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='defaul_name')
    # email = models.EmailField()
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)
    point = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)
