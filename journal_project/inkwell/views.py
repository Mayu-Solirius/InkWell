from django.shortcuts import get_object_or_404, redirect, render
from .models import JournalEntry


def index(request):
    entries = JournalEntry.objects.all().order_by("-updated_time")
    return render(request, "inkwell/index.html", {"entries": entries})


def delete_journal_entry(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    entry.delete()
    return redirect("index")
