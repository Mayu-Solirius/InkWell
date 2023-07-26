from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:pk>", views.delete_journal_entry, name="delete_journal_entry"),
]
