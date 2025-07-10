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


# Results with genre added in the url
@api_view(['GET'])
def get_genre(request):
    book_genre = request.GET.get('genre')

    if not book_genre:
        return Response({'detail': 'Parâmetro "genre" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    # Filter the answers based in the book_genre
    # We can't use `get` because genre isn't a primary key
    # Use `contains` because `genres` is a JSON field in the model
    books = Book.objects.filter(genres__icontains=f'"{book_genre}"')

    if not books.exists():
        return Response({'detail': 'Nenhum livro encontrado para esse gênero.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# Results with multiple genre added in the url
# If the book has one of the genres, it is considered a result for the endpoint
@api_view(['GET'])
def get_genres(request):
    genres = request.GET.getlist('genre')

    if not genres:
        return Response({'detail': 'Parâmetro(s) "genre" são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    # Busca por todos os gêneros como strings JSON exatas
    # Search for all genres as JSON string exactly
    query = models.Q()
    for g in genres:
        query |= models.Q(genres__icontains=f'"{g}"')

    books = Book.objects.filter(query).distinct()

    if not books.exists():
        return Response({'detail': 'Nenhum livro encontrado para os gêneros fornecidos.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# POST to save a new book
@api_view(['POST'])
def post_new_book(request):
    if request.method == 'POST':
        new_book = request.data

        serializer = BookSerializer(data=new_book)

        # Verify if the data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)