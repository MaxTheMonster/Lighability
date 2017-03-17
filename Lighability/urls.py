from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from companies import views

urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name="index"),
  url(r'^admin/', admin.site.urls),
  url(r'^home/', views.HomeView.as_view(), name="home"),
  url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
  url(r'^login/$', views.LoginView.as_view(), name="login"),
  url(r'^register/$', views.RegisterView.as_view(), name="register"),
  url(r'^new/$', views.AddCompany.as_view(), name="new_company"),
  url(r'^companies/(?P<company_id>[^/]+)/(?P<company_slug>[-\w]+)/$', views.CompanyDetail.as_view(), name="detail"),
  url(r'^companies/(?P<company_id>[^/]+)/(?P<company_slug>[-\w]+)/edit/$', views.EditCompany.as_view(), name="edit"),
  #url(r'(?P<post_id>[^/]+)', views.CompanyDetail.as_view(), name='detail'),
]


# if settings.DEBUG:
#   urlpatterns += url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#           'document_root': settings.MEDIA_ROOT,
#       }),
        
