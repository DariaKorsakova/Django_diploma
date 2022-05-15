from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
# подготовленные обобщенные вьюхи
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Product, Category, Vacancies, Comments, VacancyConditions, VacancyRequirements
from .form import ProductForm, LoginUserForm, CommentForm, VacancyForm
from .utils import ContextMixin


# для каждой вьюхи свой класс


class Index(ContextMixin, ListView):
    model = Product
    template_name = 'gastronom/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Магазин ПАРОВОЗЪ-НН')
        context.update(user_context)
        return context

    def get_queryset(self):
        queryset = Index.model.objects.all()
        return queryset


class About(ContextMixin, ListView):
    model = Product
    template_name = 'gastronom/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='О компании')
        context.update(user_context)
        return context


class Contacts(ContextMixin, ListView):
    model = Product
    template_name = 'gastronom/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Контакты')
        context.update(user_context)
        return context


class ProductIndex(ContextMixin, ListView):
    # c моделью с какой работает
    model = Product
    # с каким шаблоном
    template_name = 'gastronom/products.html'
    # название словаря, где будут все объекты из модели
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
        if self.request.GET.keys():
            # Check the search keyword
            if self.request.GET.get('src') != '':
                keyword = self.request.GET.get('src')
                if keyword is not None:
                    # Set the query set based on search keyword
                    queryset = Product.objects.filter(name__icontains=keyword.capitalize()).select_related('category')
        return queryset


# механизм проверки авторизован пользователь или нет
class CreateProduct(ContextMixin, LoginRequiredMixin, CreateView):
    # login_url = reverse_lazy('gastronom:login')
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


class ShowProduct(ContextMixin, DetailView):
    model = Product
    template_name = 'gastronom/show_product.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Детальная информация о {context['product']}")
        context.update(user_context)
        return context


class ShowCategory(ContextMixin, ListView):
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
        queryset = ShowCategory.model.objects.filter(category__slug=self.kwargs['category_slug'])
        return queryset


class VacanciesIndex(ContextMixin, ListView):
    model = Vacancies
    template_name = 'gastronom/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Вакансии')
        context.update(user_context)
        return context


class ShowVacancy(ContextMixin, DetailView):
    model = Vacancies
    template_name = 'gastronom/show_vacancy.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'vacancy_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        conditions = VacancyConditions.objects.filter(vacancies__id=context['vacancies'].id)
        requirements = VacancyRequirements.objects.filter(vacancies__id=context['vacancies'].id)
        user_context = self.get_user_context(title=f"Детальная информация о вакансии - {context['vacancies']}",
                                             conditions=conditions, requirements=requirements)
        context.update(user_context)
        return context


class CommentCreate(ContextMixin, CreateView):
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
        user_context = self.get_user_context(title='Обратная связь', button='Отправить сообщение')
        context.update(user_context)
        return context


class LoginUser(ContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'gastronom/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class CommentsIndex(ContextMixin, LoginRequiredMixin, ListView):
    raise_exception = True
    model = Comments
    template_name = 'gastronom/comments.html'
    context_object_name = 'comments'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Обратная связь')
        context.update(user_context)
        return context


class ShowComment(ContextMixin, LoginRequiredMixin, DetailView):
    model = Comments
    template_name = 'gastronom/show_comment.html'
    # переменная на которую нужно смотреть
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Детальная информация комментария")
        context.update(user_context)
        return context


class ProductDeleteView(ContextMixin, LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'gastronom/product_delete.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'
    raise_exception = True

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Удаление {context['product']}")
        context.update(user_context)
        return context


class ProductUpdateView(ContextMixin, LoginRequiredMixin, UpdateView):
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


class CreateVacancy(ContextMixin, LoginRequiredMixin, CreateView):
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


class VacancyDeleteView(ContextMixin, LoginRequiredMixin, DeleteView):
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


class VacancyUpdateView(ContextMixin, LoginRequiredMixin, UpdateView):
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
