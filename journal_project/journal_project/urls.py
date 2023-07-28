from django.contrib import admin
from django.urls import include, path
from register import views as rv

urlpatterns = [
    path("", include("inkwell.urls")),
    path("register/", rv.register, name="register"),
    path("admin/", admin.site.urls),
]
