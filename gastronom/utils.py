from .models import Category
from django.core.cache import cache


# миксин- класс который дополнительно примешивается к основному классу. Разгрузить от повторяющегося кода.
# кэширвоание- сохранение данных где-то и после запроса выдает-в постоянной памяти компьютера сохраняются
class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        #получаю категории из кэша
        cats = cache.get('categories')
        if not cats:
            cats = Category.objects.all()
            # кэш на 60 сек объект с категориями
            cache.set('categories', cats, 60)
        context['categories'] = cats
        return context
