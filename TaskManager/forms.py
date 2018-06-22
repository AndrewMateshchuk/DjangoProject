from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate
from .models import Task
import datetime


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован')
        return email

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Никнейм', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    error_massage = 'Логин или Пароль неверны'

    class Meta:
        Model = User
        fields = [
            'username',
            'password',
        ]


class TaskAddForm(ModelForm):
    title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        initial=Task.PRIORITY_MEDIUM,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}), initial=datetime.date.today())
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError('Укажите верную дату')
        return date

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'date',
            'priority',
        ]