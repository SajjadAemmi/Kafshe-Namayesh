from django.urls import include, path
from shop.urls import rest_api
from shop.urls import auth


app_name = 'shop'

urlpatterns = [
    path(r'^api/', include(rest_api)),
    path(r'^auth/', include(auth)),
]