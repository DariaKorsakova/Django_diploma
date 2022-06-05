import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
# подготовленные обобщенные вьюхи
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Product, Category, Vacancies, Comments, VacancyConditions, VacancyRequirements
from .form import ProductForm, LoginUserForm, CommentForm, VacancyForm
from .utils import ContextMixin, UserData
from unidecode import unidecode

# для каждой вьюхи свой класс
logger = logging.getLogger('main')


class Index(ContextMixin, UserData, ListView):
    model = Product
    template_name = 'gastronom/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        logger.info('Getting index page', extra=self.get_user_data())
        context = super().get_context_data()
        user_context = self.get_user_context(title='Магазин ПАРОВОЗЪ-НН')
        context.update(user_context)
        return context


class About(ContextMixin, UserData, ListView):
    model = Product
    template_name = 'gastronom/about.html'

    def get_context_data(self, **kwargs):
        logger.info('Getting about page', extra=self.get_user_data())
        context = super().get_context_data()
        user_context = self.get_user_context(title='О компании')
        context.update(user_context)
        return context


class Contacts(ContextMixin, UserData, ListView):
    model = Product
    template_name = 'gastronom/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.info('Getting contacts page', extra=self.get_user_data())
        user_context = self.get_user_context(title='Контакты')
        context.update(user_context)
        return context


class ProductIndex(ContextMixin, UserData, ListView):
    # c моделью с какой работает
    model = Product
    # с каким шаблоном
    template_name = 'gastronom/products.html'
    # название словаря, где будут все поля из модели
    context_object_name = 'products'
    # сколько объектов на странице
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Доступные товары')
        context.update(user_context)
        return context

    def get_queryset(self):
        # Сделать жадный запрос чтобы запоминалось и ускорилось полученик категорий
        queryset = ProductIndex.model.objects.all().order_by('name', 'price').select_related('category')
        logger.info('Getting products from df', extra=self.get_user_data())
        # Check the search keyword
        keyword = self.request.GET.get('src')
        if keyword is not None:
            # Set the query set based on search keyword
            queryset = Product.objects.filter(name__icontains=keyword.capitalize()).order_by(
                    'name').select_related('category')
        return queryset

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get('src')
        if keyword is not None:
            logger.info(f'Searching product {unidecode(keyword)} from df', extra=self.get_user_data())
        return super().get(self, request, *args, **kwargs)


# механизм проверки авторизован пользователь или нет
class CreateProduct(ContextMixin, UserData, LoginRequiredMixin, CreateView):
    raise_exception = True
    # работает с формой
    form_class = ProductForm
    # с каким шаблоном работает
    template_name = 'gastronom/create.html'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        # у родителя выполнить, чтобы заполнить контекст
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Добавление товара', button='Добавить товар')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Creating product {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class ShowProduct(ContextMixin, UserData, DetailView):
    model = Product
    template_name = 'gastronom/show_product.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = context['product']
        logger.info(f'Getting product page - {unidecode(product.name)}', extra=self.get_user_data())
        user_context = self.get_user_context(title=f"Детальная информация о {product}")
        context.update(user_context)
        return context


class ShowCategory(ContextMixin, UserData, ListView):
    model = Product
    template_name = 'gastronom/products.html'
    context_object_name = 'products'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug=self.kwargs['category_slug'])
        user_context = self.get_user_context(title=f"Категория: {cat.name}", slug=cat.slug, cat=cat.name)
        context.update(user_context)
        return context

    def get_queryset(self):
        cat = self.kwargs['category_slug']
        logger.info(f'Getting products from special category - {cat}', extra=self.get_user_data())
        queryset = ShowCategory.model.objects.filter(category__slug=cat).order_by(
            'name')
        return queryset


class VacanciesIndex(ContextMixin, UserData, ListView):
    model = Vacancies
    template_name = 'gastronom/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.info(f'Getting vacancies page ', extra=self.get_user_data())
        user_context = self.get_user_context(title='Вакансии')
        context.update(user_context)
        return context


class ShowVacancy(ContextMixin, UserData, DetailView):
    model = Vacancies
    template_name = 'gastronom/show_vacancy.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'vacancy_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        vac = context['vacancies']
        logger.info(f'Getting vacancies page - {unidecode(vac.name)} ', extra=self.get_user_data())
        conditions = VacancyConditions.objects.filter(vacancies__id=vac.id)
        requirements = VacancyRequirements.objects.filter(vacancies__id=vac.id)
        user_context = self.get_user_context(title=f"Детальная информация о вакансии - {vac}",
                                             conditions=conditions, requirements=requirements)
        context.update(user_context)
        return context


class CommentCreate(ContextMixin, UserData, CreateView):
    # работает с формой
    form_class = CommentForm
    # с каким шаблоном работает
    template_name = 'gastronom/create.html'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:index')

    def get_context_data(self, **kwargs):
        # у родителя выполнить, чтобы заполнить контекст
        context = super().get_context_data(**kwargs)
        logger.info(f'Getting comment page ', extra=self.get_user_data())
        user_context = self.get_user_context(title='Обратная связь', button='Отправить сообщение')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Creating comment {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class LoginUser(ContextMixin, UserData, LoginView):
    form_class = LoginUserForm
    template_name = 'gastronom/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info('Getting login page', extra=self.get_user_data())
        user_context = self.get_user_context(title='Авторизация для владельца магазина')
        context.update(user_context)
        return context

    # выполняется только если вызывается функция
    def get_success_url(self):
        return reverse('gastronom:index')


# процедура выхода
class LogoutUser(LogoutView):
    # возвращает объект только когда обращаются к next-page и потом возвращает строку(ссылку)
    next_page = reverse_lazy('gastronom:index')


class CommentsIndex(ContextMixin, UserData, LoginRequiredMixin, ListView):
    raise_exception = True
    model = Comments
    template_name = 'gastronom/comments.html'
    context_object_name = 'comments'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.info('Getting comments page', extra=self.get_user_data())
        user_context = self.get_user_context(title='Обратная связь')
        context.update(user_context)
        return context


class ShowComment(ContextMixin, LoginRequiredMixin, DetailView):
    model = Comments
    template_name = 'gastronom/show_comment.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Детальная информация комментария")
        context.update(user_context)
        return context


class ProductDeleteView(ContextMixin, LoginRequiredMixin, UserData, DeleteView):
    model = Product
    template_name = 'gastronom/product_delete.html'
    slug_url_kwarg = 'product_slug'
    raise_exception = True

    def get_success_url(self):
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Удаление {context['product']}")
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Deleting product {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class ProductUpdateView(ContextMixin, UserData, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'gastronom/create.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'
    form_class = ProductForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Изменение продукта -  {context['product']}",
                                             button='Добавить товар')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Updating product {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class CreateVacancy(ContextMixin, UserData, LoginRequiredMixin, CreateView):
    raise_exception = True
    # работает с формой
    form_class = VacancyForm
    # с каким шаблоном работает
    template_name = 'gastronom/create.html'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:vacancies')

    def get_context_data(self, **kwargs):
        # у родителя выполнить, чтобы заполнить контекст
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Добавление вакансии', button='Добавить вакансию')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Creating vacancy {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class VacancyDeleteView(ContextMixin, UserData, LoginRequiredMixin, DeleteView):
    model = Vacancies
    template_name = 'gastronom/vacancy_delete.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'vacancy_slug'
    raise_exception = True

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:vacancies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Удаление {context['vacancies']}")
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Deleting vacancy {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)


class VacancyUpdateView(ContextMixin, UserData, LoginRequiredMixin, UpdateView):
    model = Vacancies
    template_name = 'gastronom/create.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'vacancy_slug'
    form_class = VacancyForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Изменение вакансии -  {context['vacancies']}",
                                             button='Добавить вакансию')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        logger.info(f'Updating vacancy {self.request.POST}', extra=self.get_user_data())
        return super().post(self, request, *args, **kwargs)
