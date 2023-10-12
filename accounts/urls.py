from django.urls import path

from accounts.views import LoginAPIView, LogoutAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login_view"),
    path("logout/", LogoutAPIView.as_view(), name="user-logout"),
]
