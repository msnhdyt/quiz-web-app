from django.urls import path
from django.urls.conf import include
from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = []
urlpatterns = format_suffix_patterns(urlpatterns)