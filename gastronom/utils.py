from .models import Category
from django.core.cache import cache


# миксин- класс который дополнительно примешивается к основному классу. Разгрузить от повторяющегося кода.
class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('categories')
        if not cats:
            cats = Category.objects.all()
            cache.set('categories', cats, 60)
        context['categories'] = cats
        return context
