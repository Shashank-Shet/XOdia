from django.conf.urls import url
from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.LogIn.as_view(), name='login'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^play/$', views.playableUI.as_view(), name='ui'),
    url(r'^leader/$', views.LeaderBoard.as_view(), name='leader'),
    url(r'^logout/$', views.logoff, name='logout'),
    url(r'^postlogin/$', views.PostLogin.as_view(), name='postlogin'),
    url(r'^submit/$', views.GridView.as_view(), name='submit'),

]
