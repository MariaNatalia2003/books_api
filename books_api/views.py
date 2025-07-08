from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

import json

# Create your views here.

@api_view(['GET'])
def get_books(request):
    if request.method == 'GET':
        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_publisher(request, publisher):
    try:
        books = Book.objects.get(publisher=publisher)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)