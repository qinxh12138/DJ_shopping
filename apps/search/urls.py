from django.conf.urls import url
from django.contrib import admin

from apps.search import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('search_02/', views.search, name='search')
]
