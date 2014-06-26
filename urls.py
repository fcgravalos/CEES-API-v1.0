from django.conf.urls import patterns, include, url
from django.contrib import admin
from cees.views import LoginView, CheckinView, ArrivalView, GCMRegistrationView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cees.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^shopassistants/login/', LoginView.as_view(), name = 'login_view'),
    url(r'^shopassistants/checkin/', CheckinView.as_view(), name = 'checkin_view'),
    url(r'^clients/arrivals/', ArrivalView.as_view(), name = 'arrival_view'),
    url(r'^gcm/registration/', GCMRegistrationView.as_view(), name = 'gcm_reg_view')
)
