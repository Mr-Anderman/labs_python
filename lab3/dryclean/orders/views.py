from django.shortcuts import render
from .models import Contract


def archive(request):
    return render(request, 'archive.html', {"contracts": Contract.objects.all()})
