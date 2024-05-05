from django.urls import include, path
from django.http import JsonResponse
from rest_framework import routers

from shop.messages import get_messages_as_json
from shop.views.address import AddressEditView
from shop.views.cart import CartViewSet, WatchViewSet
from shop.views.checkout import CheckoutViewSet
from shop.views.catalog import ProductSelectView

router = routers.DefaultRouter()  # TODO: try with trailing_slash=False
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'watch', WatchViewSet, basename='watch')
router.register(r'checkout', CheckoutViewSet, basename='checkout')


def fetch_messages(request):
    data = get_messages_as_json(request)
    return JsonResponse({'django_messages': data})


urlpatterns = [
    path(r'^select_product/?$', ProductSelectView.as_view(), name='select-product'),
    path(r'^fetch_messages/?$', fetch_messages, name='fetch-messages'),
    path(r'^', include(router.urls)),
]