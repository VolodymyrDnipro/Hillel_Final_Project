from rest_framework import serializers
from .models import Language, Author, Category, Book, BookItem


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'language', 'category', 'quantity_in_stock']


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ['id', 'book', 'place']
