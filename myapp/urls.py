from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$',views.IndexView.as_view(), name='index'),
    url(r'^about/$',views.about,name='about'),
    url(r'^(?P<pk>\d+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^topics/$',views.topics,name='topics'),
    url(r'^course=(?P<pk>\d+)$', views.DetailView.as_view(), name='detail'),
    url(r'^topics/(?P<topic_id>\d*)$', views.topicdetail, name='topicdetail'),
    url(r'^addtopic$', views.addtopic, name='addtopic'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^mycourse/$',views.mycourse,name='mycourse'),
    url(r'^profile/$',views.viewProfile,name='profile'),
   # url(r'^reset-password/$',auth_views.password_reset,name='reset_password'),
   # url(r'^reset-password/done/$', auth_views.password_reset_done, name='password_reset_done')
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
