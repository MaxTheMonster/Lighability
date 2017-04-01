from django.conf.urls import url
from django.contrib import admin
from django.views import generic
from django.conf import settings
from companies import views
from django.conf.urls.static import static


urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name="index"),
  url(r'^home/', views.HomeView.as_view(), name="home"),
  url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
  url(r'^login/$', views.LoginView.as_view(), name="login"),
  url(r'^register/$', views.RegisterView.as_view(), name="user_register"),
  url(r'^user/(?P<username>.+)/$', views.UserProfile.as_view(), name="user_profile"),
  url(r'^user/(?P<username>.+)/edit/$', views.EditUser.as_view(), name="edit_user"),
  url(r'^new/$', views.AddCompany.as_view(), name="new_company"),
  url(r'^companies/(?P<company_id>[^/]+)/(?P<company_slug>[-\w]+)/$', views.CompanyDetail.as_view(), name="company_detail"),
  url(r'^companies/(?P<company_id>[^/]+)/(?P<company_slug>[-\w]+)/edit/$', views.EditCompany.as_view(), name="company_edit"),
  url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        
