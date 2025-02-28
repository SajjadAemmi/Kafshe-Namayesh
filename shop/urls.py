from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('products/', views.products, name='products'),
    path('products/<str:shoe_type>/', views.products_by_type, name='products_by_type'),
    path('products/<int:id>', views.product, name='product'),
    path('cart/add/<int:shoe_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:shoe_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)