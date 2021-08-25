from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, handler404
from django.contrib import admin
from django.urls import path

from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('contact/', mainapp.contact, name='contact'),
    path('admin/', admin.site.urls),
]

handler404 = 'mainapp.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

