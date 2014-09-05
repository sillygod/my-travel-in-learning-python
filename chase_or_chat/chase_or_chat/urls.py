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

urlpatterns += patterns('chase_or_chat.views',
    url(r'^meta/', 'meta_display'),
)
