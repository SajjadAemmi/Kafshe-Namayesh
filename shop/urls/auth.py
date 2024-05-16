from django.urls import include, path
from shop.views.auth import AuthFormsView, LoginView, LogoutView, PasswordChangeView, PasswordResetRequestView

urlpatterns = [
    path(r'^password/reset/?$', PasswordResetRequestView.as_view(),
        name='password-reset-request'),
    path(r'^logout/?$', LogoutView.as_view(),
        name='logout'),

]