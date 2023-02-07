from django.urls import path
from .views import RegistrationView, LoginView, LogoutView
from rest_framework.authtoken import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api-token-auth/", auth_views.obtain_auth_token),
]
