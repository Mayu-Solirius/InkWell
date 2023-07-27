from django.db import models


class JournalEntry(models.Model):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
