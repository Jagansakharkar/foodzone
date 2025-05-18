from django.contrib import admin
from django.urls import path, include
from restaurant import views

from django.conf.urls.static import static

urlpatterns = [
  path("admin/", admin.site.urls)
  , path("", include("restaurant.urls"))]
