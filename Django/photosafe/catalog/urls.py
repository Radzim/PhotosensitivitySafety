from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('photosafe.urls'))
]