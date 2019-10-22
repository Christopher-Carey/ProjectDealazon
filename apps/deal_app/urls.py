from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^sort_price$', views.sort_price),
    url(r'^current_deals$', views.deals),
    url(r'^update_price$', views.update_price),
    url(r'^add_deal$', views.add_deal),
]