from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
#    path('login', views.signin, name='login'),
#    path('signup', views.signup, name='signup'),
    path('classification', views.classification, name='classification'),
    path('generation', views.generation, name='generation'),
    url(r'^classification/savetagcontext/(?P<postpk>[0-9]+)$',views.savetagcontext, name='savetagcontext'),    
    url(r'^classification/savegeneratedtag/(?P<postpk>[0-9]+)$',views.savegeneratedtag, name='savegeneratedtag'),    
    url(r'^classification/addpost$',views.addpost, name='addpost'),    
]
