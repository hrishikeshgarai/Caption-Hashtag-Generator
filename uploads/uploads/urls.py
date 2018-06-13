from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

from core import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/$', views.simple_upload, name='simple_upload'),
    url(r'^uploads/generate/$', views.call_caption, name='generate_caption'),
    url(r'^uploads/hashtag/$', views.call_hashtag, name='generate_hashtag'),
    url(r'^uploads/activity/$', views.call_activity, name='generate_activity'),
    url(r'^uploads/location/$', views.call_location, name='generate_location'),
    url(r'^login1/$', views.login1, name='login1'),
    url(r'^log_me_in/logout1/$', views.logout1, name='logout1'),
    url(r'^log_me_in/$', views.log_me_in, name='log_me_in'),
    url(r'^sign_me_up/$', views.sign_me_up, name='sign_me_up'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'ajax/uploading$', views.upload_press, name='upload_press'),
    url(r'ajax/hashtag$', views.generate_hashtag, name='generate_hash'),
    url(r'ajax/activity$', views.generate_activity, name='generate_feelings'),
    url(r'ajax/location$', views.generate_location, name='generate_loc'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^admin/', admin.site.urls),
    url(r'^fblogin$', views.home1, name='home1'),
    url(r'^accounts/', include('allauth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
