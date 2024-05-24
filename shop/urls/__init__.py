from django.urls import include, path
from shop.urls import rest_api, auth, urls


app_name = 'shop'

urlpatterns = [
    path(r'', include(urls)),
    path(r'^api/', include(rest_api)),
    path(r'^auth/', include(auth)),
]