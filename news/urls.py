from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.article_list, name='article_list'),
    url(r'^old/$', views.article_oldlist, name='article_oldlist'),
    url(r'^value/$', views.article_evaluationlist, name='article_evaluationlist'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.article_detail, name='article_detail'),
    url(r'^article/new/$', views.article_new, name='article_new'),
    url(r'^article/(?P<pk>[0-9]+)/edit/$', views.article_edit, name='article_edit'),
    url(r'^drafts/$', views.article_draft_list, name='article_draft_list'),
    url(r'^article/(?P<pk>[0-9]+)/publish/$', views.article_publish, name='article_publish'),
    url(r'^article/(?P<pk>[0-9]+)/remove/$', views.article_remove, name='article_remove'),
    url(r'^article/(?P<pk>\d+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^comment/(?P<pk>\d+)/comment/$', views.comment_remove, name='comment_remove'),
    #signup
    url(r'^signup/$', views.signup, name='signup'),
]