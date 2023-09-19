from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Language, Author, Category, Book, BookItem
from .serializers import LanguageSerializer, AuthorSerializer, CategorySerializer, BookSerializer, BookItemSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_language(self, request, pk=None):
        data = request.data
        language_serializer = self.get_serializer(data=data)
        if language_serializer.is_valid():
            language_serializer.save()
            return Response(language_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(language_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True)
    def update_language(self, request, pk=None):
        language = self.get_object()

        data = request.data

        language_serializer = self.get_serializer(language, data=data, partial=True)
        if language_serializer.is_valid():
            language_serializer.save()
            return Response(language_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(language_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_language(self, request, pk=None):
        language = self.get_object()

        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_author(self, request):
        data = request.data
        author_serializer = self.get_serializer(data=data)
        if author_serializer.is_valid():
            author_serializer.save()
            return Response(author_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True)
    def update_author(self, request, pk=None):
        author = self.get_object()
        data = request.data
        author_serializer = self.get_serializer(author, data=data, partial=True)
        if author_serializer.is_valid():
            author_serializer.save()
            return Response(author_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_author(self, request, pk=None):
        author = self.get_object()
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_category(self, request):
        data = request.data
        category_serializer = self.get_serializer(data=data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True)
    def update_category(self, request, pk=None):
        category = self.get_object()
        data = request.data
        category_serializer = self.get_serializer(category, data=data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_category(self, request, pk=None):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_book(self, request):
        data = request.data
        book_serializer = self.get_serializer(data=data)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True)
    def update_book(self, request, pk=None):
        book = self.get_object()
        data = request.data
        book_serializer = self.get_serializer(book, data=data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response(book_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_book(self, request, pk=None):
        book = self.get_object()
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_book_item(self, request):
        data = request.data
        book_item_serializer = self.get_serializer(data=data)
        if book_item_serializer.is_valid():
            book_item_serializer.save()
            return Response(book_item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True)
    def update_book_item(self, request, pk=None):
        book_item = self.get_object()
        data = request.data
        book_item_serializer = self.get_serializer(book_item, data=data, partial=True)
        if book_item_serializer.is_valid():
            book_item_serializer.save()
            return Response(book_item_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(book_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_book_item(self, request, pk=None):
        book_item = self.get_object()
        book_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
