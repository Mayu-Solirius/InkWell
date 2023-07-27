from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("save/", views.save_journal_entry, name="save_journal_entry"),
    path("delete/<int:pk>", views.delete_journal_entry, name="delete_journal_entry"),
]
