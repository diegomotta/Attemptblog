from django.conf.urls import url
from django.contrib import admin


from .views import post_create, post_detail,post_list,post_update,post_delete

urlpatterns = [
    url(r'^create/$', "gym.views.post_create"),
    url(r'^(?P<slug>[\w-]+)/$', "gym.views.post_detail",name='post-detail'),
    url(r'^$', "gym.views.post_list", name='List'),
    url(r'^(?P<slug>[\w-]+)/edit/$', "gym.views.post_update", name='post-update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', "gym.views.post_delete", name='post-delete'),
    
]