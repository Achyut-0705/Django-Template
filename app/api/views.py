from rest_framework.response import Response
from rest_framework import generics
# Create your views here.

def View(request, *args, **kwargs):
    return Response({'message': 'Hello, World!'})