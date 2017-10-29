from django.conf.urls import url
from . import views

urlpatterns = [
    #login START
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    #login END
    url(r'^poke_process',views.poke_process),
]