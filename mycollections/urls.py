from django.conf.urls import url
from . import views

app_name = 'mycollections'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<signlanguage_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<huruf_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^hurufs/(?P<filter_by>[a-zA_Z]+)/$', views.hurufs, name='hurufs'),
    url(r'^create_signlanguage/$', views.create_signlanguage, name='create_signlanguage'),
    url(r'^(?P<signlanguage_id>[0-9]+)/create_huruf/$', views.create_huruf, name='create_huruf'),
#   url(r'^(?P<signlanguage_id>[0-9]+)/edit_huruf/(?<huruf_id>[0-9]+)/$', views.edit_huruf, name='edit_huruf'),
    url(r'^(?P<signlanguage_id>[0-9]+)/delete_huruf/(?P<huruf_id>[0-9]+)/$', views.delete_huruf, name='delete_huruf'),
    url(r'^(?P<signlanguage_id>[0-9]+)/favorite_signlanguage/$', views.favorite_signlanguage, name='favorite_signlanguage'),
    url(r'^(?P<signlanguage_id>[0-9]+)/delete_signlanguage/$', views.delete_signlanguage, name='delete_signlanguage'),
]
