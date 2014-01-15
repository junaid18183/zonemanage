from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'zonemanage.views.home', name='home'),
     url(r'^zone_list/$', 'zonemanage.views.view_zone_list', name="zone_list"),
     url(r'^zone_detail/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.view_zone_detail', name="zone_detail"),
     url(r'^editsoa/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.edit_soa1', name="edit_soa"),
     url(r'^savesoa/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.save_soa', name="save_soa"),
     url(r'^editzone/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.edit_zone', name="edit_zone"),
     url(r'^savezone/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.save_zone', name="save_zone"),
     url(r'^reloadzone/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.reload_zone', name="save_zone"),
)
