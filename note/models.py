from django.db import models
from django.contrib.auth.models import User



class Note(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    writer = models.ForeignKey(User ,on_delete=models.CASCADE, related_name='writer_relate')
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribing', null=True, blank=True)
    # subscribers = models.ManyToManyField(User, related_name='')

    def __str__(self) -> str:
        return self.title
