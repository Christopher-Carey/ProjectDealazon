from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.root),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.login_page),
    url(r'^logout$', views.logout),
]