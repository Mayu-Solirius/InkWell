from django.shortcuts import render
from .models import JournalEntry


def index(request):
    entries = JournalEntry.objects.all().order_by("-updated_time")
    return render(request, "inkwell/index.html", {"entries": entries})
