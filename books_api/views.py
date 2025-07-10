from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

import json

# Create your views here.

# Return all books in the database
@api_view(['GET'])
def get_books(request):
    if request.method == 'GET':
        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)

# Results with publisher added in the url
@api_view(['GET'])
def get_publisher(request):
    publisher_name = request.GET.get('publisher')

    if not publisher_name:
        return Response({'detail': 'Parâmetro "publisher" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    # Filter the answers based in the publisher_name
    # We can't use `get` because publisher isn't a primary key
    books = Book.objects.filter(publisher=publisher_name)

    if not books.exists():
        return Response({'detail': 'Nenhum livro encontrado para essa editora.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
