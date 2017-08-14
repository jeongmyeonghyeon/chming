"""chming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^', apis.PostListView.as_view()),
    url(r'^img/$', apis.PostImageListView.as_view()),
    url(r'^notice/$', apis.PostNoticeListView.as_view()),
    url(r'^create/$', apis.PostCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveView.as_view()),
    url(r'^(?P<pk>\d+)/update/$', apis.PostUpdateView.as_view()),
    url(r'^(?P<pk>\d+)/delete/$', apis.PostDestroyView.as_view()),

    url(r'^(?P<pk>\d+)/comment/$', apis.CommentListView.as_view()),
    url(r'^(?P<pk>\d+)/comment/create/$', apis.CommentCreateView.as_view()),
    url(r'^comment/(?P<pk>\d+)/delete/$', apis.CommentDestroyView.as_view()),

]
