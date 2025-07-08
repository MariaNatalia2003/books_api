from rest_framework import serializers

from .models import Book

# Serializers send the data to frontend and generate JSON's from the Models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'