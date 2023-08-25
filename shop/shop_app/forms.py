from .models import Language, Author
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Your Name'})
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'subject', 'placeholder': 'Subject'})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'message', 'placeholder': 'Message'}))
    sender_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Your Email'}))


class BookFilterForm(forms.Form):
    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    price_ranges = forms.MultipleChoiceField(choices=[
        ('0-30', '$0 - $30'),
        ('30-50', '$30 - $50'),
        ('50-80', '$50 - $80'),
        ('80-120', '$80 - $120'),
        ('120-', '$120 and above')
    ],
        widget=forms.CheckboxSelectMultiple,
        required=False)
