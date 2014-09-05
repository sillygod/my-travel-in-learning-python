from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from books.models import Book
from django.template import RequestContext
from django.core.mail import send_mail
from books.form import ContactForm
import markdown
from markdown.extensions import codehilite


def search_form(request):
    if 'q' in request.POST:
            query = request.POST['q']
            if query:
                books = Book.objects.filter(title__icontains=query)
                return render(request, 'search_result.html', {'books': books, 'query': query})
            else:
                return render(request, 'search_form.html', {'error': True})
    else:
        return render(request, 'search_form.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})


def md(request):
    return render(request, 'live_markdown.html')


def pro_markdown(request):
    if request.method == 'POST':
        context = request.POST['context']
        print(context)
        html = markdown.markdown(context, extensions=[
            'codehilite', 'fenced_code'], extension_configs={
            'codehilite':{
                        'noclasses': True}
            })
        return HttpResponse(html)
