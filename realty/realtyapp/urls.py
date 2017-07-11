from django.conf.urls import include, url
from realtyapp.views import IndexView, AddRealtyView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url('^add/', AddRealtyView.as_view(), name='add_realty'),
]
