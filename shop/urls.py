from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Маршрутизатор

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gastronom.urls'))  # нужно смотреть адреса в этом приложении

]

# Как сделать для сайта, а не для дебага???? как показать ссылку туда
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
