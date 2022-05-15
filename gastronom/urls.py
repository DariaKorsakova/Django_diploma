from django.urls import path


from . import views

# views.ProductIndex.as_view() превращение класса в функцию
app_name = 'gastronom'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contact_us', views.CommentCreate.as_view(), name='contact_us'),
    path('about', views.About.as_view(), name='about'),
    path('products', views.ProductIndex.as_view(), name='products'),
    path('contacts', views.Contacts.as_view(), name='contacts'),
    path('vacancies', views.VacanciesIndex.as_view(), name='vacancies'),
    path('show_product_info/<slug:product_slug>', views.ShowProduct.as_view(), name='show_product'),
    path('show_category/<slug:category_slug>', views.ShowCategory.as_view(), name='show_category'),
    path('show_vacancy_info/<slug:vacancy_slug>', views.ShowVacancy.as_view(), name='show_vacancy'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('comments', views.CommentsIndex.as_view(), name='comments'),
    path('show_comment/<int:pk>', views.ShowComment.as_view(), name='show_comment'),
    path('create_product', views.CreateProduct.as_view(), name='create_product'),
    path('show_product_info/<slug:product_slug>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('show_product_info/<slug:product_slug>/update', views.ProductUpdateView.as_view(), name='product_update'),
    path('create_vacancy', views.CreateVacancy.as_view(), name='create_vacancy'),
    path('show_vacancy_info/<slug:vacancy_slug>/delete', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('show_vacancy_info/<slug:vacancy_slug>/update', views.VacancyUpdateView.as_view(), name='vacancy_update'),

]

