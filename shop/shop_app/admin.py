from django.contrib import admin
from .models import Language, Author, Category, Book, Cart, CartItem, Order, OrderItem, CarouselSlide

admin.site.register(CarouselSlide)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'language', 'category', 'publication_date', 'price', 'quantity_in_stock', 'is_visible')
    list_filter = ('author', 'language', 'category', 'is_visible')
    search_fields = ('title', 'author__name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_price', 'is_ordered')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'unit_price')
