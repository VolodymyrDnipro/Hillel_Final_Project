from django.contrib import admin
from .models import Language, Author, Category, Book, BookItem

admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookItem)
