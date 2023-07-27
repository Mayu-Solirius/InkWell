from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import JournalEntry
from .forms import JournalEntryForm


def index(request):
    entries = JournalEntry.objects.all().order_by("-updated_time")
    return render(request, "inkwell/index.html", {"entries": entries})


def delete_journal_entry(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    entry.delete()
    return redirect("index")


def save_journal_entry(request):
    if request.method == "POST":
        entry_id = request.POST.get("entry_id")
        if entry_id == "0":
            # Create a new entry
            form = JournalEntryForm(request.POST)
        else:
            # Update an existing entry
            entry = JournalEntry.objects.get(pk=entry_id)
            form = JournalEntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})

    return redirect("journal_entry_list")
