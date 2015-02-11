# django
from django.shortcuts import render
from django.http import HttpResponse
# thrid-party
import markdown


def md(request):
    return render(request, 'live_markdown.html')


def pro_markdown(request):
    if request.method == 'POST':
        context = request.POST['context']
        print(context)
        html = markdown.markdown(
            context,
            extensions=['codehilite', 'fenced_code'],
            extension_configs={
                'codehilite': {'noclasses': True}
            })
        return HttpResponse(html)
