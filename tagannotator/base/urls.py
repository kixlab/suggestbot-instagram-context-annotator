from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('signin', TemplateView.as_view(template_name='base/signin.html')),
    path('createsession', views.create_session, name='create_session'),
    url(r'^(?P<sessionpk>[0-9]+)/selectsource',TemplateView.as_view(template_name='base/selectsource.html')),    
    path('<int:sessionpk>/accountinfo/',TemplateView.as_view(template_name='base/accountinfo.html')),    
    path('<int:sessionpk>/accountinfo/saveaccount/',views.saveaccount, name='saveaccount'),    
    path('<int:sessionpk>/postinfo/',TemplateView.as_view(template_name='base/postinfo.html'), name='postinfo'),    
    path('<int:sessionpk>/postinfo/checkpost/',views.checkpost, name='checkpost'),
    path('<int:sessionpk>/postinfo/addpost/',views.addpost, name='addpost'),

    path('<int:sessionpk>/post/<int:postpk>/classification/<str:originalpostid>/',views.classification, name='classification'),    
    path('<int:sessionpk>/post/<int:postpk>/generation/<str:originalpostid>/',views.generation, name='classification'),    
    



    url(r'^(?P<sessionpk>[0-9]+)/choosedevice',TemplateView.as_view(template_name='base/choosedevice.html')),    

    path('generation', views.generation, name='generation'),
    path('upload', views.BasicUploadView.as_view(), name='upload'),
    url(r'^classification/savetagcontext/(?P<postpk>[0-9]+)$',views.savetagcontext, name='savetagcontext'),    
    url(r'^classification/savegeneratedtag/(?P<postpk>[0-9]+)$',views.savegeneratedtag, name='savegeneratedtag'),   
]
