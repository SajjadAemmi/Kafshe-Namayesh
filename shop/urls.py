from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('details/<int:id>', views.details, name='details'),
    path('a2/', views.b2, name='c2'),
    path('testing/', views.testing, name='testing'),
]
