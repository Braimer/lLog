from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    #a topic the user is learning about
    text=models.CharField(max_length=500)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)#topic belong to specific user

    def __str__(self):
        #return a string representation of the model
        return self.text

class Entry(models.Model):
    #something specific learned about a topic
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateField(auto_now_add=True)

    '''nesting a meta class inside entry class ,holds extra information
    for managing a model,allow to set special attribute telling django
    to use Entries when refering to many,without it (Entrys )would be case'''

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        #return a string representation of the model,what to show
        return f"{self.text[:50]}..."