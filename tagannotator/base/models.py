from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.timezone import now

class Session(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    starttime=models.DateTimeField(default=None, blank=True)
    endtime=models.DateTimeField(default=None, blank=True)
    status=models.BooleanField(default=False, blank=True)
    token=models.CharField(max_length=50, default=None, null=True, blank=True)
    def __str__(self):
        return self.user.username+"-"+str(self.starttime)

class Post(models.Model):
    session=models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    SOURCES=[
        ('instagram', 'instagram'),
        ('upload', 'upload')
    ]
    source=models.CharField(max_length=20, choices=SOURCES, null=True, blank=True)
    tagdone=models.BooleanField(default=False, blank=True, null=True)
    contextdone=models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        return self.session.user.username +" - "+self.source +str(self.pk)

class InstagramAccount(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    session=models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    hashed_account_id=models.CharField(max_length=200)
    suspicious=models.BooleanField(default=False)
    duplicated=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + " - " + self.hashed_account_id

class InstaPost(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed_post_url=models.CharField(max_length=200)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return str(self.post.pk) + " - " +self.hashed_post_url

def user_directory_path(instance, filename):
    userid=instance.session.user.username
    sessionpk=instance.session.pk
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/session_{1}/{2}'.format(userid,sessionpk, filename)

class Photo(models.Model):
    session=models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
#    title = models.CharField(max_length=255, blank=True)
#    user=models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name.split('/')[2]

class UploadPost(models.Model):
    uploadedphoto=models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.post) +" - " + str(self.uploadedphoto)


class Context(models.Model):
    label=models.CharField(max_length=50)
    exampletags=models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.label

class Tag(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text=models.CharField(max_length=150)
    MADEBY=[
        ('user', 'user'),
        ('post', 'post')
    ]
    madeby=models.CharField(max_length=20, choices=MADEBY, null=True, blank=True, default='post')
    def __str__(self):
        return str(self.post.pk) +" - "+ self.text +" - "+self.madeby

class Mapping(models.Model):
    tag=models.ForeignKey(Tag, on_delete=models.CASCADE)
    context=models.ForeignKey(Context, on_delete=models.CASCADE)
    def __str__(self):
        return self.tag.text +" - "+ self.context.label

class ClassificationLog(models.Model):
    logs=models.CharField(max_length=9999999)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return 'Log for '+ str(self.post.pk)

