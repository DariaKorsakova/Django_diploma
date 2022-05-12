from django.contrib import admin
from django.urls import path, include

# Маршрутизатор

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gastronom.urls'))  # нужно смотреть адреса в этом приложении

]
