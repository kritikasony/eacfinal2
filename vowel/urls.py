from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Register.as_view(), name='Register'),
    url(r'^login/$', views.Login.as_view(), name='Login'),
    url(r'^logout/$', views.Logout.as_view(), name='Logout'),
    # url(r'^word/', views.getword, name='word'),
    url(r'^get-soundfiles/$', views.AjaxGetSoundFiles.as_view(), name='AjaxGetSoundFiles'),
    url(r'^play/$', views.index, name='index'),
]