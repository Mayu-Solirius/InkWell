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
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if not title and not content:
            # If both title and content are empty, remove the entry from the database
            if entry_id != "0":
                entry = get_object_or_404(JournalEntry, pk=entry_id)
                entry.delete()
            return JsonResponse({"status": "success"})

        if entry_id == "0":
            # Create a new entry only if either title or content is not empty
            if title or content:
                form = JournalEntryForm(request.POST)
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "errors": {
                            "non_field_errors": [
                                "Both title and content cannot be empty."
                            ]
                        },
                    }
                )
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
