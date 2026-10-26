from django.shortcuts import render
from django import template


from django.http import HttpResponse
def home(request):
    return render(request, 'templates/static_handler.html')

def hello(request):
    return HttpResponse(u'Химчистка "Бриллиант" - Ювелирная точность при удалении загрязнений')
