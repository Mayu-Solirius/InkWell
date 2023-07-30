from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import JournalEntry
from .forms import JournalEntryForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by("-updated_time")
    return render(request, "inkwell/index.html", {"entries": entries})


@login_required
def delete_journal_entry(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    # Check if the user owns the journal entry
    if entry.user != request.user:
        return JsonResponse(
            {
                "status": "error",
                "message": "You can only delete your own journal entries.",
            }
        )

    entry.delete()
    return redirect("index")


@login_required
def save_journal_entry(request):
    form = None

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
                # Link the new entry to the currently logged-in user
                form = JournalEntryForm(request.POST)
                new_entry = form.save(commit=False)
                new_entry.user = request.user
                new_entry.save()
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
            # Check if the user owns the journal entry
            if entry.user != request.user:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "You can only edit your own journal entries.",
                    }
                )

            form = JournalEntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})

    return redirect("index")
