from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader, RequestContext
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm, PhotoForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
import operator
import random
import string
import json



@csrf_exempt
def create_session(request):
    username=request.POST.get('username',None)
    user_check = User.objects.filter(username__iexact=username)
    if len(user_check)==0:
        user = User.objects.create_user(username=username, password=username)
    else:
        user=user_check[0]
    # create new session 
    starttime=timezone.now()
    session=Session(user=user, starttime=starttime,endtime=starttime, status=False)
    session.save()
    sessionurl='/session/'+str(session.pk)
    login(request,user)
    print("hihi", sessionurl)
    return HttpResponse(session.pk)

@csrf_exempt
def saveaccount(request, sessionpk):
    user=request.user
    instaid=request.POST.get('instaid',None)
    stringsuspicious=request.POST.get('suspicious',None)
    if(stringsuspicious=='false'):
        suspicious=False
    else:
        suspicious=True
    # check if duplicate, if ducplicate, check if same user 
    accounts_check=InstagramAccount.objects.all()
    duplicate=False
    for account_check in accounts_check:
        if(check_password(instaid, account_check.hashed_account_id)):
            duplicate=True
            existing_user=account_check.user
            if(user!=existing_user):
                account=InstagramAccount(user=user, hashed_account_id=make_password(instaid), suspicious=True, duplicated=True)
                account.save()
        #    print("Duplicated")
    if not duplicate:
        account=InstagramAccount(user=user, hashed_account_id=make_password(instaid), suspicious=suspicious, duplicated=False)
        account.save()
       # print("New user")
    return HttpResponse('')

@csrf_exempt
def checkpost(request, sessionpk):
    if request.method=="POST":
        user=request.user
        userid=request.POST.get('userid',None)
        posturl=request.POST.get('posturl', None)
        # check if the username match existing instagram account
        account_check=InstagramAccount.objects.filter(user=user)
        checkresult='invaliduser'
        for registered_account in account_check:
            if (check_password(userid,registered_account.hashed_account_id)):
                checkresult='validuser'
                break
        if(checkresult=='validuser'):# owner ok 
            # now check if this post has been used before 
            posts_check=InstaPost.objects.filter(user=user)
            for post_check in posts_check:
                if(check_password(posturl, post_check.hashed_post_url)):
                    checkresult='duplicated'
                    break
        return HttpResponse(json.dumps({'checkresult':checkresult}),content_type="application/json")

@csrf_exempt
def addpost(request, sessionpk):
    if request.method=="POST":
        source=request.POST.get('source',None)
        user=request.user 
        thissession=Session.objects.get(pk=sessionpk)

        newPost=Post(session=thissession, source=source)
        newPost.save()

        if(source=='instagram'):
            posturl=request.POST.get('posturl',None)
            newInstaPost=InstaPost(hashed_post_url=make_password(posturl), post=newPost)
            newInstaPost.save()
        if(source=='upload'):
            uploadedphotopk=request.POST.get('uploadedphotopk',None)
            uploadedphoto=Photo.objects.get(pk=uploadedphotopk)
            newUsedPhoto=UsedPhoto(uploadedphoto=uploadedphoto, post=newPost)
            newUsedPhoto.save()
        return HttpResponse(json.dumps({'postpk': newPost.pk}),content_type="application/json")

@csrf_exempt
def classification(request, sessionpk, postpk, originalpostid):
    user=request.user
    thissession=Session.objects.get(pk=sessionpk)
    contexts=Context.objects.all()
    context={
        'contexts': contexts,
        'session': thissession,
        'originalpostid':originalpostid,
    }
    
    return render(request, 'base/classification.html', context)

@csrf_exempt
def generation(request):
    user=request.user
    context={}
    return render(request, 'base/generation.html',context)


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'base/upload.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse({'message': 'Success'})


@csrf_exempt
def savetagcontext(request, postpk):
    user=request.user

    tags=request.POST.getlist('tags[]')
    contexts=request.POST.getlist('contexts[]')
    
    thisPost=Post.objects.get(pk=postpk)

    for i in range(len(tags)):
        tag=tags[i]
        context=contexts[i]
        thisContext=Context.objects.get(label=context)
        newTag=Tag(post=thisPost, text=tag, madeat='post')
        newTag.save()
        newMapping=Mapping(tag=newTag, context=thisContext)
        newMapping.save()
    return HttpResponseRedirect('')

@csrf_exempt
def savegeneratedtag(request, postpk):
    tags=request.POST.getlist('tags[]')
    contexts=request.POST.getlist('contexts[]')
    
    thisPost=Post.objects.get(pk=postpk)

    for i in range(len(tags)):
        tag=tags[i]
        context=contexts[i]
        thisContext=Context.objects.get(label=context)
        newTag=Tag(post=thisPost, text=tag,madeat='generated')
        newTag.save()
        newMapping=Mapping(tag=newTag, context=thisContext)
        newMapping.save()

    return HttpResponse('')