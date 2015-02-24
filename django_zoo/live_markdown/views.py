# django
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# thrid-party
import markdown


class MarkDownView(TemplateView):

    template_name = 'live_markdown/base.html'


def parse_markdown(request):
    '''receive a json post.
    ex.
        {'context': the content of markdown...}
    '''
    if request.method == 'POST':
        context = request.POST['context']
        html = markdown.markdown(
            context,
            extensions=['codehilite', 'fenced_code'],
            extension_configs={
                'codehilite': {'noclasses': True}
            }
        )
        return HttpResponse(html)
