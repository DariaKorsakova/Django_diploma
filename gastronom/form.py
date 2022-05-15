from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, FileInput, TextInput, NumberInput, Select, Textarea, EmailInput, CharField, \
    PasswordInput, CheckboxSelectMultiple, ModelMultipleChoiceField, SelectMultiple
from .models import Product, Comments, Vacancies, VacancyRequirements, VacancyConditions


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Для формирован всех полей
        super(ProductForm, self).__init__(*args, **kwargs)
        # Обновление лейблов
        self.fields['name'].label = 'Название товара'
        self.fields['category'].label = 'Категория товара'
        self.fields['category'].empty_label = 'Категория товара не выбрана'
        self.fields['description'].label = 'Описание товара'
        self.fields['price'].label = 'Цена товара'
        self.fields['image'].label = 'Изображение товара'
        # убрать двоиточия с конца
        self.label_suffix = ''

    # настройки

    class Meta:
        model = Product
        # Перечисление полей, которые нужно отобразить
        fields = ['category', 'name', 'description', 'image', 'price']
        # Описание полей - каждый виджет - для описания атрибутов тега
        widgets = {
            'category': Select(attrs={
                'class': 'form-select'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена товара'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание товара'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Изображение товара'
            })
        }

    def clean_name(self):
        # получить проверенное значение
        name = self.cleaned_data['name']
        if len(name) < 4:
            # вызов ошибки у name
            self.add_error('name', 'Слишком короткое имя. Название должно содержать более 4 знаков!')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            self.add_error('description', 'Слишком короткое описание. Описание должно содержать более 10 знаков!')
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if not (0 < price <= 10000):
            self.add_error('price', 'Некорректная цена!')
        return price


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['email'].label = 'Email'
        self.fields['message'].label = 'Сообщение'
        # убрать двоиточия с конца
        self.label_suffix = ''

    class Meta:
        # Определяем модель, на основе которой создаем форму
        model = Comments
        # Поля, которые будем использовать для заполнения
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'

            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта'
            }),
            'message': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напишите тут ваше сообщение'
                }
            )
        }

        def clean_first_name(self):
            # получить проверенное значение
            first_name = self.cleaned_data['first_name']
            if len(first_name) < 1:
                # вызов ошибки у name
                self.add_error('name', 'Слишком короткое имя')
            return first_name

        def clean_message(self):
            message = self.cleaned_data['message']
            if len(message) < 5:
                self.add_error('message', 'Слишком короткое сообщение. Сообщение должно содержать более 5 знаков!')
            return message


class VacancyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)
        # Обновление лейблов
        self.fields['name'].label = 'Название вакансии'
        self.fields['description'].label = 'Описание вакансии'
        self.fields['conditions'].label = 'Условия'
        self.fields['requirements'].label = 'Требования'
        self.label_suffix = ''

    class Meta:
        model = Vacancies
        fields = ['name', 'description', 'conditions', 'requirements']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название вакансии'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание вакансии'
            }),
            'conditions': SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Условия'
                }),
            'requirements': SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Требования'
                })
        }


class LoginUserForm(AuthenticationForm):
    # Создаем поля моделей
    username = CharField(
        label='Логин',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин'

        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',

        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        # автоматическое добавление модели юзера- возвращает объект модели из настроек
        model = get_user_model()
        fields = ['username', 'password1']
