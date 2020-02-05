from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('start', TemplateView.as_view(template_name='base/start.html')),
    path('signin', TemplateView.as_view(template_name='base/signin.html')),
    path('createsession', views.create_session, name='create_session'),
    path('<int:sessionpk>/selectsource',TemplateView.as_view(template_name='base/selectsource.html')),    

    # instagram 
    path('<int:sessionpk>/instagram/accountinfo/',views.accountinfo, name='accountinfo'),    
    path('<int:sessionpk>/instagram/postinfo/',TemplateView.as_view(template_name='base/postinfo.html')),    
    path('<int:sessionpk>/instagram/postinfo/checkpost/',views.checkpost, name='checkpost'),
    path('<int:sessionpk>/instagram/postinfo/addposts/',views.addposts, name='addposts'),
    path('<int:sessionpk>/instagram/addtags/<int:postorder>/',views.addtags, name='addtags'),   
    path('<int:sessionpk>/instagram/classification/instruction/',TemplateView.as_view(template_name='base/classification_instruction.html'), name='classification_instruction'),    
    path('<int:sessionpk>/instagram/classification/<int:postorder>/',views.classification, name='classification'),
    path('<int:sessionpk>/instagram/classification/finish/',views.finish, name='finish'),    

    # image upload
    path('<int:sessionpk>/upload/',views.BasicUploadView.as_view(), name='upload'),    
    path('<int:sessionpk>/upload/delete/',views.deletephoto, name='deletephoto'),       
    path('<int:sessionpk>/upload/getphotos/',views.getphotos, name='getphotos'),  
    path('<int:sessionpk>/upload/createposts/',views.createposts_upload, name='createposts_upload'), 
    path('<int:sessionpk>/upload/generatetags/<int:uploadpostorder>/',views.generatetags, name='generatetags'),    
    path('<int:sessionpk>/upload/classification/instruction/',TemplateView.as_view(template_name='base/classification_instruction.html'), name='classification_instruction'),    
    path('<int:sessionpk>/upload/classification/<int:uploadpostorder>/',views.classification_upload, name='classification_upload'),

    # end page
    path('<int:sessionpk>/upload/classification/finish/',views.finish, name='finish'),    

    # image upload from other device 
    path('<int:sessionpk>/otherdevice/',TemplateView.as_view(template_name='base/choosedevice.html')),    
]
