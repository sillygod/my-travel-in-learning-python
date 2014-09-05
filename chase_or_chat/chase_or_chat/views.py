from django.http import HttpResponse



def meta_display(request):

    html = []
    for key in request.META:
        html.append('<div><span>{} </span><span> {}</span></div>'.format(
                    key, request.META[key]))

    return HttpResponse(''.join(html))
