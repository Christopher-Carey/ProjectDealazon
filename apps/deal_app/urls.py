from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^sort$', views.deals),
    url(r'^add_deal$', views.add_deal),
]