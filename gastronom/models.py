# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField('Имя', max_length=20, unique=True, db_index=True)
    slug = models.SlugField('URL товара', max_length=20, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    # Описаны
    # поля
    # модели
    # с
    # типами
    # данных


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField('Название', max_length=50, null=False)
    # внешние ключи, нельзя удалить пока есть товары в категории
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    description = models.TextField('Описание товара', max_length=10000, null=False)
    price = models.FloatField('Цена товара')
    image = models.ImageField('Изображение', upload_to='gastronom')
    #  slug это уникальная строка идентификатор, понятная человеку. добавление индекс на слаг
    slug = models.SlugField('URL товара', max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

    # создание автоматического слага в форме+с учетом порядкого номера для разных товаров с одинаковым названием
    def save(self, *args, **kwargs):
        last_obj = Product.objects.all().order_by('id').last()
        if last_obj:
            last_pk = last_obj.pk + 1
        else:
            last_pk = 1
        string = unidecode(str(self.name) + '_' + str(last_pk))
        # слагификация
        self.slug = slugify(string)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gastronom:show_product', kwargs={'product_slug': self.slug})

    # замена названия объектов на названия товаров(строковое представления объекта)

    def __str__(self):
        return self.name


class VacancyConditions(models.Model):
    objects = models.Manager()
    name = models.TextField('Условие', db_index=True)

    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = "Условия"

    def __str__(self):
        return self.name


class VacancyRequirements(models.Model):
    objects = models.Manager()
    name = models.TextField('Требование', db_index=True)

    class Meta:
        verbose_name = 'Требование'
        verbose_name_plural = "Требования"

    def __str__(self):
        return self.name


class Vacancies(models.Model):
    objects = models.Manager()
    name = models.CharField('Название', max_length=40, db_index=True)
    description = models.TextField('Описание', db_index=True)
    conditions = models.ManyToManyField(VacancyConditions, verbose_name='Условия')
    requirements = models.ManyToManyField(VacancyRequirements, verbose_name='Требования')
    slug = models.SlugField('URL вакансии', max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = "Вакансии"

    def get_absolute_url(self):
        return reverse('gastronom:show_vacancy', kwargs={'vacancy_slug': self.slug})

    def save(self, *args, **kwargs):
        last_obj = Vacancies.objects.all().order_by('id').last()
        if last_obj:
            last_pk = last_obj.pk + 1
        else:
            last_pk = 1
        string = unidecode(str(self.name) + '_' + str(last_pk))
        # слагификация
        self.slug = slugify(string)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comments(models.Model):
    objects = models.Manager()
    first_name = models.CharField('Имя', max_length=200)
    last_name = models.CharField('Фамилия', max_length=200)
    email = models.EmailField('Email', max_length=200)
    message = models.TextField('Сообщение', max_length=1000)
    created_date = models.DateTimeField('Время публикации', auto_now=True)

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ('-created_date', )

    def __str__(self):
        return self.email
