from django.conf.urls import patterns, url

from videoRepository import views


urlpatterns = patterns	(	'',
							url(r'^$', views.VRIndex.as_view()),
							url(r'^UserRepository/(?P<username>.*)/$', views.UserRepository.as_view()),
							url(r'^logout/$', views.Logout.as_view()),
							url(r'^upload/(?P<username>.*)/$', views.UploadFiles.as_view()),
						)

