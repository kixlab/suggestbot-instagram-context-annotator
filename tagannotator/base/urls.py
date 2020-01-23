from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('signin', TemplateView.as_view(template_name='base/signin.html')),
    path('createsession', views.create_session, name='create_session'),
    path('<int:sessionpk>/selectsource',TemplateView.as_view(template_name='base/selectsource.html')),    

    # instagram 
    path('<int:sessionpk>/instagram/accountinfo/',views.accountinfo, name='accountinfo'),    
    path('<int:sessionpk>/instagram/postinfo/',views.postinfo, name='postinfo'),    
#    path('<int:sessionpk>/instagram/postinfo/',TemplateView.as_view(template_name='base/postinfo.html'), name='postinfo'),    
    path('<int:sessionpk>/instagram/postinfo/checkpost/',views.checkpost, name='checkpost'),
    path('<int:sessionpk>/instagram/postinfo/addpost/',views.addpost, name='addpost'),
    path('<int:sessionpk>/instagram/createposts/',views.createposts, name='createposts'), 
#    path('<int:sessionpk>/instagram/addtags/<int:postorder>/',views.addtags, name='addtags'),   

    path('<int:sessionpk>/post/<int:postpk>/classification/<str:originalpostid>/savetagcontext/',views.savetagcontext, name='savetagcontext'),    

    # image upload
    path('<int:sessionpk>/upload/',views.BasicUploadView.as_view(), name='upload'),    
    path('<int:sessionpk>/upload/delete/',views.deletephoto, name='deletephoto'),       
    path('<int:sessionpk>/upload/getphotos/',views.getphotos, name='getphotos'),  
    path('<int:sessionpk>/upload/createposts/',views.createposts_upload, name='createposts_upload'), 
    path('<int:sessionpk>/upload/generatetags/<int:uploadpostorder>/',views.generatetags, name='generatetags'),    
    path('<int:sessionpk>/upload/classification/instruction/',TemplateView.as_view(template_name='base/classification_instruction.html'), name='classification_instruction'),    
    path('<int:sessionpk>/upload/classification/<int:uploadpostorder>/',views.classification_upload, name='classification_upload'),

    path('<int:sessionpk>/upload/classification/finish/',views.finish, name='finish'),    

    # image upload from other device 
    path('<int:sessionpk>/otherdevice/',TemplateView.as_view(template_name='base/choosedevice.html')),    
]


## Upload 상황에서 hashtag 다 만들고, 그다음 classification instruction 갔다가 그 다음 다시 첫 포스트부터 classification 하게 해라 

## Instagram upload 1개에서 5개로 바꾸고, 각각에 대해서 바로 post 만든 다응메, upload일 때와 마찬가지로 taggeneration 이후 classification으로 
