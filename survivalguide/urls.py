from django.conf.urls import include, url
from django.contrib import admin

from .views import HomePageView
from .views import SignUpView
from .views import LoginView
from .views import LogOutView

urlpatterns = [
    # Examples:
    # url(r'^$', 'survivalguide.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogOutView.as_view(), name='logout'),
    url(r'^talks/', include('talks.urls', namespace='talks')),
]
