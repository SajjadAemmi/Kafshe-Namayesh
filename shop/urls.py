from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('products/', views.products, name='products'),
    path('products/<int:id>', views.product, name='product'),
    path('a2/', views.b2, name='c2'),
    path('testing/', views.testing, name='testing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)