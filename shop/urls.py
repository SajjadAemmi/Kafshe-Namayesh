from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/type/<str:shoe_type>/', views.products, name='products_by_type'),
    path('products/category/<str:shoe_category>/', views.products, name='products_by_category'),
    path('products/type/<str:shoe_type>/category/<str:shoe_category>/', views.products, name='products_by_type_and_category'),
    path('products/<int:id>', views.product, name='product'),
    path('cart/add/<int:shoe_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:shoe_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/shipping/', views.order_detail, name='order_detail'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/profile/", views.profile, name="profile"),
    path("orders/", views.order_list, name="orders"),
    path('bankgateways/', az_bank_gateways_urls()),
    path("go-to-bank-gateway/", views.go_to_gateway_view, name="go-to-bank-gateway"),
    path("callback-gateway/", views.callback_gateway_view, name="callback-gateway"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
