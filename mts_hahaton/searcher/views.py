from django.http import HttpResponse
from rest_framework.views import APIView


def hello_world(request):
    return HttpResponse("hello, world!")

