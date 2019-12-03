from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader, RequestContext
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
import operator
import random
import string
import json
import datetime

@csrf_exempt
def classification(request):
    user=request.user
    contexts=Context.objects.all()
    context={
        'contexts': contexts
    }
    return render(request, 'base/classification.html',context)

@csrf_exempt
def generation(request):
    user=request.user
    context={}
    return render(request, 'base/generation.html',context)

@csrf_exempt
def addpost(request):
    user=request.user
    newPost=Post(user=user)
    newPost.save()
    curpk=newPost.pk
    return HttpResponse(curpk)


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