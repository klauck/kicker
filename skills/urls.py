"""kicker URL Configuration

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
from skills import views

urlpatterns = [
    url(r'^$', views.current_season, name='current_season'),
    url(r'^table/(?P<begin_date_str>\d{4}-\d{2}-\d{2})/(?P<end_date_str>\d{4}-\d{2}-\d{2})$', views.table, name='table'),
    url(r'^player/(?P<player_id>[0-9]+)/(?P<begin_date_str>\d{4}-\d{2}-\d{2})/(?P<end_date_str>\d{4}-\d{2}-\d{2})$', views.player, name='player'),
]
