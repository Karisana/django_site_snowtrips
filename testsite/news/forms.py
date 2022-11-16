from .models import News, Category
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=200, label='Ваше имя:',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(min_length=30,max_length=200, label='Тема письма:',
                              help_text='Обязательное поле. Минимум 30, но не более 200 символов.',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(max_length=5000, label='Текст письма:',
                              help_text='Обязательное поле. Не более 5000 символов.',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    email = forms.EmailField(label='Email',
                                     widget=forms.EmailInput(attrs={'class': 'form-control'}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Логин:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Логин',
                               help_text='Обязательное поле. Не более 100 символов. Только буквы, цифры и символы '
                                         '@/./+/-/_.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(min_length=3, max_length=40, label='Имя пользователя',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                help_text='Пароль не должен быть слишком похож на другую вашу личную информацию.\n'
                                          'Ваш пароль должен содержать как минимум 8 символов.\n'
                                          'Пароль не должен быть слишком простым и распространенным.\n'
                                          'Пароль не может состоять только из цифр.',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', help_text='Введите пароль ещё раз для подтверждения.',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'id_email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__' -  будут представлены все поля модели NEWS
        fields = ['title', 'quotation', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'quotation': forms.Textarea(attrs={
                'class': 'form-control',
                'id': "exampleFormControlTextarea1",
                'rows': '2',
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'id': "exampleFormControlTextarea1",
                'rows': '5',
            }),

            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    # проверка title на ошибки, например на начало заголовка с цифры. Можно править размер, регистр и так далее.
    # Если проверка не продет, то данные сохраняться не будут.
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 120 or len(title) < 10:
            # if re.match(r'\d', title):
            raise ValidationError('Длина заголовка должна быть больше 10, но не больше 120 символов')
        return title

    def clean_quotation(self):
        quotation = self.cleaned_data['quotation']
        if len(quotation) > 113 or len(quotation) < 50:
            raise ValidationError('Длина цитаты должна быть больше 50, но не больше 113 символов')
        return quotation

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 5000 or len(content) < 300:
            raise ValidationError('Длина цитаты должна быть больше 300, но не больше 5000 символов')
        return content

# не связанная c моделью форма  :

# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150,
#                             label='Название статьи',
#                             widget=forms.TextInput(attrs={
#                                 'class': 'form-control',
#                             }))
#
#     quotation = forms.CharField(max_length=300,
#                                 label='Короткая цитата из статьи',
#                                 widget=forms.Textarea(attrs={
#                                     'class': 'form-control',
#                                     'id': "exampleFormControlTextarea1",
#                                     'rows': '2',
#                                 }))
#
#     content = forms.CharField(label='Текст статьи',
#                               widget=forms.Textarea(attrs={'class': 'form-control',
#                                                            'id': "exampleFormControlTextarea1",
#                                                            'rows': "5"}))
#
#     category = forms.ModelChoiceField(empty_label='Выберите категорию:',
#                                       label='Категория',
#                                       queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={'class': 'form-control'}))
#
#     is_published = forms.BooleanField(label='Опубликовать?', initial=True)
