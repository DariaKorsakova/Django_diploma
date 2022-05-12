from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
# подготовленные обобщенные вьюхи
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Product, Category, Vacancies, Contact
from .form import ProductForm, ContactForm, LoginUserForm
from .utils import ContextMixin


# для каждой вьюхи свой класс

# class Index(SingleTableView):
#     table_class = ProductTable
#     queryset = Product.objects.all()
#     template_name = 'gastronom/index.html'
#     context_object_name = 'products'


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
        queryset = ProductIndex.model.objects.all().order_by('name', 'price')
        if self.request.GET.keys():
            # Check the search keyword
            if self.request.GET.get('src') != '':
                keyword = self.request.GET.get('src')
                if keyword is not None:
                    # Set the query set based on search keyword
                    queryset = Product.objects.filter(
                        Q(name__icontains=keyword.capitalize()) | Q(description__icontains=keyword.capitalize()))
        return queryset


# механизм проверки авторизован пользователь или нет
class CreateProduct(ContextMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('gastronom:login')
    # работает с формой
    form_class = ProductForm
    # с каким шаблоном работает
    template_name = 'gastronom/create_product.html'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        # у родителя выполнить, чтобы заполнить контекст
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Добавление товара')
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
        user_context = self.get_user_context(title=f"Категория: {cat.name}", slug=cat.slug)
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
        user_context = self.get_user_context(title=f"Детальная информация о вакансии - {context['vacancies']}")
        context.update(user_context)
        return context


class ContactCreate(ContextMixin, CreateView):
    # работает с формой
    form_class = ContactForm
    # с каким шаблоном работает
    template_name = 'gastronom/contact_us.html'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:index')

    def get_context_data(self, **kwargs):
        # у родителя выполнить, чтобы заполнить контекст
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Обратная связь')
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
    login_url = reverse_lazy('gastronom:login')
    model = Contact
    template_name = 'gastronom/comments.html'
    context_object_name = 'comments'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title='Обратная связь')
        context.update(user_context)
        return context


class ShowComment(ContextMixin, DetailView):
    model = Contact
    template_name = 'gastronom/show_comment.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'comment_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Детальная информация комментария")
        context.update(user_context)
        return context


class ProductDeleteView(ContextMixin, DeleteView):
    model = Product
    template_name = 'gastronom/product_delete.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Удаление {context['product']}")
        context.update(user_context)
        return context


class ProductUpdateView(ContextMixin, UpdateView):
    model = Product
    template_name = 'gastronom/create_product.html'
    # переменная на которую нужно смотреть
    slug_url_kwarg = 'product_slug'
    form_class = ProductForm

    def get_success_url(self):
        # перенаправление на главную страницу
        return reverse('gastronom:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_context = self.get_user_context(title=f"Изменение продукта -  {context['product']}")
        context.update(user_context)
        return context
