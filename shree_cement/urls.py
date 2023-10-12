"""Shree Cement URL Configuration."""
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("slct/manage/", admin.site.urls),
    path("data/", include("analytical_data.urls")),
    path("accounts/", include("accounts.urls")),
    path("sso/", include("django_auth_adfs.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
