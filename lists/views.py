# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(
        request, 'home.html', {
        'new_item_text': request.POST.get('item_text', '')
        }
    )
