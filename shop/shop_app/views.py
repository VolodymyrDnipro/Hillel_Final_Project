from django.db.models import Q, Sum
from django.views.generic import ListView, DetailView, FormView, TemplateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from random import sample
from decimal import Decimal
from django import forms
from django.db import transaction

from .forms import RegisterForm, BookFilterForm, FeedbackForm
from .models import Category, CarouselSlide, Book, Cart, CartItem, UserProfile, User, OrderItem, Order
from django.conf import settings


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'context'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and 'book_id' in request.POST:
            book_id = request.POST['book_id']
            book = Book.objects.get(id=book_id)

            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect('shop_app:index')

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = {}

        all_books = list(Book.objects.all())
        if all_books:
            random_books = sample(all_books, 8)
            context['random_books'] = random_books

        all_slides = list(CarouselSlide.objects.all())
        if all_slides:
            random_slides = sample(all_slides, 3)
            context['random_slides'] = random_slides



        categories = Category.objects.all()
        if categories:
            random_categories = sample(list(categories), min(len(categories), 10))
            context['random_categories'] = random_categories

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0

        return context


class ContactView(View):
    template_name = 'other/contact.html'

    def get(self, request, *args, **kwargs):
        form = FeedbackForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['sender_email']
            admin_email = settings.ADMINS[0][1]  # Assuming the first admin email is used

            send_mail(
                subject,
                message,
                sender_email,
                [admin_email],
                fail_silently=False,
            )

            return redirect('feedback_success')  # Assuming you have a success page

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}

        categories = Category.objects.all()
        if categories:
            random_categories = sample(list(categories), min(len(categories), 10))
            context['random_categories'] = random_categories
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context


class BooksListView(ListView):
    model = Book
    template_name = 'shop/books_list.html'
    context_object_name = 'books'
    paginate_by = 8
    ordering = ['-publication_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        random_categories = sample(list(categories), min(len(categories), 10))

        context['random_categories'] = random_categories
        context['filter_form'] = BookFilterForm(self.request.GET)

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        form = BookFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['languages']:
                queryset = queryset.filter(language__in=form.cleaned_data['languages'])
            if form.cleaned_data['authors']:
                queryset = queryset.filter(author__in=form.cleaned_data['authors'])

            price_ranges = form.cleaned_data['price_ranges']
            if price_ranges:
                price_filters = Q()  # Initialize an empty Q object to build OR conditions
                for price_range in price_ranges:
                    min_price, max_price = map(int, price_range.split('-'))
                    if max_price == 0:
                        price_filters |= Q(price__lte=min_price)
                    else:
                        price_filters |= Q(price__gte=min_price, price__lte=max_price)

                queryset = queryset.filter(price_filters)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        sort_param = self.request.GET.get('sort', 'latest')
        if sort_param == 'low_price':
            queryset = queryset.order_by('price')
        elif sort_param == 'high_price':
            queryset = queryset.order_by('-price')

        category_id = self.request.GET.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(category=category)

        return queryset


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = ''


class LoginRequiredColorMixin(LoginRequiredMixin):
    login_url = '/login/'


class RegisterFormView(generic.FormView):
    template_name = "registration/registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy("shop_app:index")

    def form_valid(self, form):
        user = form.save()

        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if categories:
            categories = Category.objects.all()
            random_categories = sample(list(categories), min(len(categories), 10))

        context['random_categories'] = random_categories
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'order/cart.html'
    login_url = 'shop_app:login'

    def post(self, request, *args, **kwargs):
        book_id_to_delete = request.POST.get('book_id_to_delete')

        user_cart = Cart.objects.filter(user=self.request.user).first()
        if user_cart and book_id_to_delete:
            cart_item_to_delete = CartItem.objects.filter(cart=user_cart, book_id=book_id_to_delete).first()
            if cart_item_to_delete:
                cart_item_to_delete.delete()
        return redirect('shop_app:cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_cart = Cart.objects.filter(user=self.request.user).first()
        if user_cart:
            cart_items = CartItem.objects.filter(cart=user_cart)
            context['cart_items'] = cart_items

            for cart_item in cart_items:
                cart_item.total_price = cart_item.book.price * cart_item.quantity
                cart_item.save()

            subtotal_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)
            context['subtotal_price'] = subtotal_price

            shipping_price = subtotal_price * Decimal('0.1')
            context['shipping_price'] = shipping_price

            total_price = subtotal_price + shipping_price
            context['total_price'] = total_price

        categories = Category.objects.all()
        if categories:
            random_categories = sample(list(categories), min(len(categories), 10))
            context['random_categories'] = random_categories
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/user_profile.html'
    context_object_name = 'user'
    login_url = 'shop_app:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        context['user_profile'] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': user_profile.mobile,
            'address': user_profile.address,
            'country': user_profile.country,
            'city': user_profile.city,
            'state': user_profile.state,
            'zip': user_profile.zip,
        }

        categories = Category.objects.all()
        if categories:
            random_categories = sample(list(categories), min(len(categories), 10))
            context['random_categories'] = random_categories

        if user.is_authenticated:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile', 'address', 'country', 'city', 'state', 'zip']


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    second_form_class = UserProfileUpdateForm
    template_name = "profile/update_profile.html"
    success_url = reverse_lazy('shop_app:user_profile')
    login_url = reverse_lazy('shop_app:login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = self.form_class(self.request.POST, instance=self.object)
            context['profile_form'] = self.second_form_class(self.request.POST, instance=self.object.userprofile)
        else:
            context['user_form'] = self.form_class(instance=self.object)
            context['profile_form'] = self.second_form_class(instance=self.object.userprofile)
        return context

    def form_valid(self, form):
        user_form = self.form_class(self.request.POST, instance=self.object)
        profile_form = self.second_form_class(self.request.POST, instance=self.object.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'order/checkout.html'
    login_url = 'shop_app:login'

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user_cart = Cart.objects.filter(user=request.user).first()
            if user_cart:
                cart_items = CartItem.objects.filter(cart=user_cart)
                total_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)

                order = Order.objects.create(user=request.user, total_price=total_price)

                for cart_item in cart_items:
                    OrderItem.objects.create(order=order, book=cart_item.book, quantity=cart_item.quantity,
                                             unit_price=cart_item.book.price)

                cart_items.delete()
                user_cart.delete()

        return redirect('shop_app:order_confirmation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_cart = Cart.objects.filter(user=self.request.user).first()
        if user_cart:
            cart_items = CartItem.objects.filter(cart=user_cart)
            context['cart_items'] = cart_items

            for cart_item in cart_items:
                cart_item.total_price = cart_item.book.price * cart_item.quantity
                cart_item.save()

            subtotal_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)
            context['subtotal_price'] = subtotal_price

            shipping_price = subtotal_price * Decimal('0.1')
            context['shipping_price'] = shipping_price

            total_price = subtotal_price + shipping_price
            context['total_price'] = total_price

        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = UserProfileUpdateForm(instance=self.request.user.userprofile)

        categories = Category.objects.all()
        if categories:
            random_categories = sample(list(categories), min(len(categories), 10))
            context['random_categories'] = random_categories
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_items_count = cart.cartitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                context['cart_items_count'] = cart_items_count if cart_items_count else 0
        return context


class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'order/order_confirmation.html'
    login_url = 'shop_app:login'
