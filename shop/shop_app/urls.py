from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, LogoutView

handler404 = 'shop_app.views.page_not_found'
app_name = 'shop_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('books/', views.BooksListView.as_view(), name='books_list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/checkout', views.CheckoutView.as_view(), name='checkout'),
    path('order_confirmation/', views.OrderConfirmationView.as_view(), name='order_confirmation'),


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("profile/", views.UserDetailView.as_view(), name="user_profile"),
    path("registration/", views.RegisterFormView.as_view(), name="registration"),
    path("update_profile/", views.UserUpdateView.as_view(), name="update_profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
