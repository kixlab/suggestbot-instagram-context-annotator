from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.timezone import now

class Context(models.Model):
    label=models.CharField(max_length=50)
    exampletags=models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.label

class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username +" - "+str(self.pk)

class Tag(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text=models.CharField(max_length=150)
    MADEAT=[
        ('post', 'post'),
        ('generated', 'generated')
    ]
    madeat=models.CharField(max_length=20, choices=MADEAT, null=True, blank=True)
    def __str__(self):
        return str(self.post.pk) +" - "+ self.text +" - "+self.madeat

class Mapping(models.Model):
    tag=models.ForeignKey(Tag, on_delete=models.CASCADE)
    context=models.ForeignKey(Context, on_delete=models.CASCADE)
    def __str__(self):
        return self.tag.text +" - "+ self.context.label


