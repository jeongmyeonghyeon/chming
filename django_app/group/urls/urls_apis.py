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
from django.conf.urls import url, include
from django.contrib import admin

from ..apis import group, group_search, region, hobby

urlpatterns = [
    # Group API
    url(r'^$', group.MainGroupListView.as_view()),
    url(r'^all/$', group.AllGroupListView.as_view()),
    url(r'^register/$', group.GroupRegisterView.as_view()),
    url(r'^(?P<pk>\d+)/$', group.GroupRetrieveView.as_view()),
    url(r'^(?P<group_pk>\d+)/edit/$', group.GroupUpdateView.as_view()),
    url(r'^(?P<group_pk>\d+)/delete/$', group.GroupDestroyView.as_view()),
    url(r'^(?P<group_pk>\d+)/like_toggle/$', group.GroupLikeToggleView.as_view()),
    url(r'^(?P<group_pk>\d+)/join/$', group.GroupJoinView.as_view()),
    url(r'^validate_name/$', group.IsValidNameView.as_view()),

    # Group Search API
    url(r'^search/', group_search.GroupSearchView.as_view()),

    # Post API
    url(r'^(?P<group_pk>\d+)/post/', include('post.urls.urls_apis')),

    # Region API
    url(r'^region/$', region.RegionListCreateView.as_view()),
    url(r'^region/(?P<pk>\d+)/$', region.RegionUpdateDestroyView.as_view()),

    # Hobby API
    url(r'^hobby/$', hobby.HobbyListCreateView.as_view()),
    url(r'^hobby/(?P<pk>\d+)/$', hobby.HobbyUpdateDestroyView.as_view())
]
