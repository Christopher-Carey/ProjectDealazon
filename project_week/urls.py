from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.login_app.urls')),
    url(r'^deals/', include('apps.deal_app.urls')),
]