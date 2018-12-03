from django.conf.urls import url, include
import xadmin
from apps.main import views

urlpatterns = [
    url('xadmin/',xadmin.site.urls),
    url('^$', views.index, name='first'),
    url('detail_01/', include('detail.urls')),
    url('search_01/', include('search.urls')),
    url('account/', include('account.urls')),
    url('cart/', include('cart.urls')),
]
