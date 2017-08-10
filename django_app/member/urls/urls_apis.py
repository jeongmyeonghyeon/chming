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
    url(r'^$', apis.UserListView.as_view()),
    # Auth = Signup/login/logout
    url(r'^signup/$', apis.UserSignupView.as_view()),
    url(r'^login/$', apis.ObtainAuthToken.as_view()),
    url(r'^logout/$', apis.Logout.as_view()),
    # User - Detail/Delete
    url(r'^(?P<pk>\d+)/$', apis.UserRetrieveDestroyView.as_view()),
    # User - Update
    url(r'^(?P<pk>\d+)/edit/$', apis.UserUpdateView.as_view()),

]