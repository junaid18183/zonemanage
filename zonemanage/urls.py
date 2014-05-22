from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.htm'}),
     url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name' :'logout.htm'}),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'zonemanage.views.home', name='home'),
     url(r'^zone_list/$', 'zonemanage.views.view_zone_list', name="zone_list"),
     url(r'^zone_detail/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.view_zone_detail', name="zone_detail"),
     url(r'^editsoa/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.edit_soa', name="edit_soa"),
     url(r'^editzone/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.edit_zone', name="edit_zone"),
     url(r'^reloadzone/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.reload_zone', name="reload_zone"),
     url(r'^history/(?P<zonename>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.archive_list', name="archive_list"),
     url(r'^load_archive/(?P<zonename>[a-zA-Z0-9.-]+)/(?P<archive>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.load_archive', name="load_archive"),
     url(r'^revert_archive/(?P<zonename>[a-zA-Z0-9.-]+)/(?P<archive>[a-zA-Z0-9.-]+)/$', 'zonemanage.views.revert_archive', name="revert_archive"),
)
