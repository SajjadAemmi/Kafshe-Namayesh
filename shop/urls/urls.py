from django.urls import path
from shop.views import client


urlpatterns = [
    path('', client.index, name='index'),
    path('members/', client.members, name='members'),
    path('members/details/<int:id>', client.details, name='details'),
    path('details/<int:id>', client.details, name='details'),
    path('a2/', client.b2, name='c2'),
    path('testing/', client.testing, name='testing'),
]
