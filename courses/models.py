from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save

from .utils import slug_generator

User = settings.AUTH_USER_MODEL

# Create your models here.
class Subject(models.Model):
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    overview    = models.TextField()
    # many owners
    #access key
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def subject_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(subject_pre_save_receiver, sender=Subject)

class Module(models.Model):
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    description = models.TextField()
    # ordering
    created     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    