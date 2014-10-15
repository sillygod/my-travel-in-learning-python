from django.conf.urls import patterns, include, url
from books.models import Publisher

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list_page.html',
}


urlpatterns = patterns('books.views',
    # Examples:
    # url(r'^$', 'chase_or_chat.views.home', name='home'),
    # url(r'^chase_or_chat/', include('chase_or_chat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^search-form/', 'search_form'),
    url(r'^md/', 'md'),
    url(r'^pro_markdown/', 'pro_markdown'),
    url(r'^contact/', 'contact'),
    # url(r'^meta/', chase_or_chat.views.meta_display),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('data_grabber.views',
    url(r'^add_to_db/$', 'add_to_db'),
    url(r'^add_prod/(?P<page>\d*)/$', 'add_prod'),
    url(r'^add_prod/$', 'add_prod'),
    url(r'^home/$', 'show_home'),
    url(r'^show_prod/(?P<page>\d*)/$', 'show_prod'),
    url(r'^search/$', 'search'),
)

urlpatterns += patterns('chase_or_chat.views',
    url(r'^meta/', 'meta_display'),
)
