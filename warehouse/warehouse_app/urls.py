from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LanguageViewSet, AuthorViewSet, CategoryViewSet, BookViewSet, BookItemViewSet

app_name = 'warehouse_app'

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-items', BookItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    path('languages/create/', views.LanguageViewSet.as_view({'post': 'create_language'}), name='language-create'),
    path('languages/update/<int:pk>/', views.LanguageViewSet.as_view({'put': 'update_language'}),
         name='language-update'),
    path('languages/delete/<int:pk>/', views.LanguageViewSet.as_view({'delete': 'delete_language'}),
         name='language-delete'),

    path('authors/create/', views.AuthorViewSet.as_view({'post': 'create_author'}), name='author-create'),
    path('authors/update/<int:pk>/', views.AuthorViewSet.as_view({'put': 'update_author'}), name='author-update'),
    path('authors/delete/<int:pk>/', views.AuthorViewSet.as_view({'delete': 'delete_author'}), name='author-delete'),

    path('categories/create/', views.CategoryViewSet.as_view({'post': 'create_category'}), name='category-create'),
    path('categories/update/<int:pk>/', views.CategoryViewSet.as_view({'put': 'update_category'}),
         name='category-update'),
    path('categories/delete/<int:pk>/', views.CategoryViewSet.as_view({'delete': 'delete_category'}),
         name='category-delete'),

    path('books/create/', views.BookViewSet.as_view({'post': 'create_book'}), name='book-create'),
    path('books/update/<int:pk>/', views.BookViewSet.as_view({'put': 'update_book'}), name='book-update'),
    path('books/delete/<int:pk>/', views.BookViewSet.as_view({'delete': 'delete_book'}), name='book-delete'),

    path('book-items/create/', views.BookItemViewSet.as_view({'post': 'create_book_item'}), name='bookitem-create'),
    path('book-items/update/<int:pk>/', views.BookItemViewSet.as_view({'put': 'update_book_item'}),
         name='bookitem-update'),
    path('book-items/delete/<int:pk>/', views.BookItemViewSet.as_view({'delete': 'delete_book_item'}),
         name='bookitem-delete'),
]
