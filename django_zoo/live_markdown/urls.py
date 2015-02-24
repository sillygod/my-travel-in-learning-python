from django.conf.urls import patterns, include, url
from django.contrib import admin
from live_markdown.views import MarkDownView, parse_markdown

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', view=MarkDownView.as_view(), name='home'),  # omg, '^$' this
    # is so important
    url(r'^parse_markdown/$', view=parse_markdown, name='parse_markdown'),
)