# Register your models here.
from django.contrib import admin

from .models import Product, Category, Vacancies, Comments, VacancyConditions, VacancyRequirements


# конфигурационный класс - настраивает админку


class ProductAdmin(admin.ModelAdmin):
    # какие поля отображать
    list_display = ('id', 'name', 'slug', 'price')
    # где ссылки на товар
    list_display_links = ('id', 'name')
    # поиск по
    search_fields = ('name', 'description', 'price')
    # slug привязывается к названию- ставится запятая чтобы сделать кортеж
    prepopulated_fields = {'slug': ('name', )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class VacanciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'message', 'email')
    list_display_links = ('id', 'message')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vacancies, VacanciesAdmin)
admin.site.register(VacancyRequirements)
admin.site.register(VacancyConditions)
admin.site.register(Comments, CommentsAdmin)