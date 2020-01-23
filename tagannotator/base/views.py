from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
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
from django.utils.encoding import smart_str

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
    token='temp token'
    session=Session(user=user, starttime=starttime,endtime=starttime, status=False, token=token)
    session.save()
    sessionurl='/session/'+str(session.pk)
    login(request,user)
    print("hihi", sessionurl)
    return HttpResponse(session.pk)

@csrf_exempt
def accountinfo(request, sessionpk):
    user=request.user
    thissession=Session.objects.get(pk=sessionpk)
    if request.method=="GET":
        return render(request, 'base/accountinfo.html', {})
    if request.method=="POST":
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
                    ## same insta id submitted by 2+MTurkers 
                    account=InstagramAccount(user=user, session=thissession, hashed_account_id=make_password(instaid), suspicious=True, duplicated=True)
                    account.save()
            #    print("Duplicated")
        if not duplicate:
            account=InstagramAccount(user=user, session=thissession, hashed_account_id=make_password(instaid), suspicious=suspicious, duplicated=False)
            account.save()
        # print("New user")
        return HttpResponse('')

def postinfo(request, sessionpk):
    user=request.user
    thissession=Session.objects.get(pk=sessionpk)
    if request.method=="GET":
        return render(request, 'base/postinfo.html', {})

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
def createposts(request, sessionpk):
    user=request.user 
    thissession=Session.objects.get(pk=sessionpk)
    if request.method=="POST":
        posturls_string=request.POST.get('posturls', None)
        posturls=json.loads(posturls)

    photos_list = Photo.objects.filter(session=thissession)
    first=''
    if(len(photos_list)<4):
        return HttpResponse(json.dumps({'result':False}),content_type="application/json")
    else:
        for photo in photos_list:
            newpost=Post(session=thissession, source='upload')
            newpost.save()
            newup=UploadPost(uploadedphoto=photo, post=newpost)
            newup.save()
        return HttpResponse(json.dumps({'result':True}),content_type="application/json")



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
    tags=Tag.objects.filter(post__session=thissession)
    context={
        'contexts': contexts,
        'session': thissession,
        'originalpostid':originalpostid,
        'tagscount': len(tags)
    }
    
    return render(request, 'base/classification.html', context)


@csrf_exempt
def savetagcontext(request, sessionpk, postpk, originalpostid):
    user=request.user
    post=Post.objects.get(pk=postpk)
    stringtagcontext=request.POST.get('tagcontext', None)
    madeby=request.POST.get('madeby', None)

    tagcontexts=json.loads(stringtagcontext)
    for tagcontext in tagcontexts:
        hashtagtext=tagcontext['hashtag']
        newtag=Tag(post=post, text=hashtagtext, madeby=madeby)
        newtag.save()
        print(hashtagtext, madeby)
        contexts=tagcontext['context']
        for context in contexts:
            context=Context.objects.get(label=context)
            newMapping=Mapping(tag=newtag, context=context)
            newMapping.save()
    print(tagcontext)
    return HttpResponseRedirect('')


@csrf_exempt
def generation(request):
    user=request.user
    context={}
    return render(request, 'base/generation.html',context)


class BasicUploadView(View):
    def get(self, request, sessionpk):
        thissession=Session.objects.get(pk=sessionpk)
        photos_list = Photo.objects.filter(session=thissession)
        return render(self.request, 'base/upload.html', {'photos': photos_list})

    def post(self, request, sessionpk):
        thissession=Session.objects.get(pk=sessionpk)
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo=Photo(session=thissession, file=form.cleaned_data["file"])
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name.split('/')[2], 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

@csrf_exempt
def deletephoto(request, sessionpk):
    if request.method=="POST":
        photopk=request.POST.get('photopk',None)
        user=request.user 
        thissession=Session.objects.get(pk=sessionpk)

        photo=Photo.objects.get(pk=photopk)
        photo.delete()
        return HttpResponse('')

@csrf_exempt
def getphotos(request, sessionpk):
    if request.method=="GET":
        user=request.user 
        thissession=Session.objects.get(pk=sessionpk)
        photos_list = Photo.objects.filter(session=thissession)
        photos_data=[]
        for photo in photos_list:
            photos_data.append({"pk":photo.pk, "filename":smart_str(photo.file.name).split('/')[2], "url":photo.file.url})
        photos_json=json.dumps(photos_data,ensure_ascii=False)
        return JsonResponse(photos_json, safe=False)

@csrf_exempt
def createposts_upload(request, sessionpk):
    user=request.user 
    thissession=Session.objects.get(pk=sessionpk)
    photos_list = Photo.objects.filter(session=thissession)
    first=''
    if(len(photos_list)<4):
        return HttpResponse(json.dumps({'result':False}),content_type="application/json")
    else:
        for photo in photos_list:
            newpost=Post(session=thissession, source='upload')
            newpost.save()
            newup=UploadPost(uploadedphoto=photo, post=newpost)
            newup.save()
        return HttpResponse(json.dumps({'result':True}),content_type="application/json")

@csrf_exempt
def generatetags(request, sessionpk, uploadpostorder):
    user=request.user 
    thissession=Session.objects.get(pk=sessionpk)
    thisuploadpost=UploadPost.objects.filter(uploadedphoto__session=thissession).order_by('pk')[uploadpostorder-1]
    if request.method=="GET":
        return render(request, 'base/generatetags.html', {'post': thisuploadpost, 'postorder':uploadpostorder})
    if request.method=="POST":
        thispost=thisuploadpost.post
        oldtags=Tag.objects.filter(post=thispost)
        for oldtag in oldtags:
            oldtag.delete()
        hashtags=json.loads(request.POST.get('hashtags',None))
        for hashtag in hashtags: 
            newtag=Tag(post=thispost, text=hashtag, madeby='user')
            newtag.save()
        return HttpResponse(json.dumps({'result':True}),content_type="application/json")



@csrf_exempt
def classification_upload(request, sessionpk, uploadpostorder):
    user=request.user 
    thissession=Session.objects.get(pk=sessionpk)
    thisuploadpost=UploadPost.objects.filter(uploadedphoto__session=thissession).order_by('pk')[uploadpostorder-1]
    thispost=thisuploadpost.post
    if request.method=="GET":
        tags=Tag.objects.filter(post=thispost)
        contexts=Context.objects.all()
        context={
            'post': thispost,
            'contexts': contexts,
            'uploadpost':thisuploadpost,
            'tags': tags,
            'postorder':uploadpostorder
        }
        return render(request, 'base/classification.html', context)
    if request.method=="POST":
        mappings=json.loads(request.POST.get('mappings',None))
        for mapping in mappings:
            tagpk=mapping["hashtag"]
            selectedcontextpks=mapping["context"]
            curtag=Tag.objects.get(pk=tagpk)
            for selectedcontextpk in selectedcontextpks:
                curcontext=Context.objects.get(pk=selectedcontextpk)
                newmapping=Mapping(tag=curtag, context=curcontext)
                newmapping.save()
                print('Hi', tagpk, selectedcontextpk)
        return HttpResponse(json.dumps({'result':True}),content_type="application/json")


@csrf_exempt
def finish(request, sessionpk):
    user=request.user 
    thissession=Session.objects.get(pk=sessionpk)
    token=thissession.token
    thissession.status=True 
    return render(request, 'base/finish.html',{'token':token})
    