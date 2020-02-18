from django.conf import settings
from django.shortcuts import render


def demo(request):
    return render(request, "demo.html", {'settings': settings})
