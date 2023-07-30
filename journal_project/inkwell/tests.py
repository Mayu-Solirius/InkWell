from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from inkwell.models import JournalEntry
from factory import Factory, Faker
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    password = make_password("testpassword")


class JournalEntryFactory(DjangoModelFactory):
    class Meta:
        model = JournalEntry

    user = UserFactory()
    title = Faker("sentence", nb_words=4)
    content = Faker("paragraph")


class JournalAppTestCase(TestCase):
    # Create some test users and journal entries
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        self.entry1 = JournalEntryFactory(user=self.user1)
        self.entry2 = JournalEntryFactory(user=self.user1)
        self.entry3 = JournalEntryFactory(user=self.user2)

    # Test if journal entries are properly associated with users
    def test_journal_entries(self):
        self.assertEqual(self.entry1.user, self.user1)
        self.assertEqual(self.entry2.user, self.user1)
        self.assertEqual(self.entry3.user, self.user2)

    # Test deleting a journal entry
    def test_delete_journal_entry(self):
        self.client.login(username=self.user1.username, password="testpassword")

        entry_count_before_delete = JournalEntry.objects.count()
        response = self.client.post(f"/delete/{self.entry1.pk}")
        entry_count_after_delete = JournalEntry.objects.count()

        self.assertEqual(entry_count_after_delete, entry_count_before_delete - 1)
        self.assertEqual(response.status_code, 302)

    # Test editing a journal entry
    def test_edit_journal_entry(self):
        self.client.login(username=self.user1.username, password="testpassword")
        edited_entry_data = {
            "entry_id": str(self.entry2.pk),
            "title": "Edited Entry Title",
            "content": "Edited entry content.",
        }
        response = self.client.post("/save/", edited_entry_data)

        self.assertEqual(response.status_code, 200)

        updated_entry = JournalEntry.objects.get(pk=self.entry2.pk)

        self.assertEqual(updated_entry.title, "Edited Entry Title")
        self.assertEqual(updated_entry.content, "Edited entry content.")

    # Test to see if an updated journal entry with no content and title is deleted
    def test_delete_empty_journal_entry(self):
        self.client.login(username=self.user2.username, password="testpassword")
        entry_count_before_delete = JournalEntry.objects.count()
        edited_entry_data = {
            "entry_id": str(self.entry3.pk),
            "title": "",
            "content": "",
        }
        response = self.client.post("/save/", edited_entry_data)
        self.assertEqual(response.status_code, 200)
        entry_count_after_delete = JournalEntry.objects.count()
        self.assertEqual(entry_count_after_delete, entry_count_before_delete - 1)

    # Test editing a journal entry with no title
    def test_remove_journal_entry_title(self):
        self.client.login(username=self.user2.username, password="testpassword")
        edited_entry_data = {
            "entry_id": str(self.entry3.pk),
            "title": "",
            "content": str(self.entry3.content),
        }
        response = self.client.post("/save/", edited_entry_data)

        self.assertEqual(response.status_code, 200)

        updated_entry = JournalEntry.objects.get(pk=self.entry3.pk)

        self.assertEqual(updated_entry.title, "")
        self.assertEqual(updated_entry.content, str(self.entry3.content))

    # Test editing a journal entry with no content
    def test_remove_journal_entry_content(self):
        self.client.login(username=self.user2.username, password="testpassword")
        edited_entry_data = {
            "entry_id": str(self.entry3.pk),
            "title": str(self.entry3.title),
            "content": "",
        }
        response = self.client.post("/save/", edited_entry_data)

        self.assertEqual(response.status_code, 200)

        updated_entry = JournalEntry.objects.get(pk=self.entry3.pk)

        self.assertEqual(updated_entry.title, str(self.entry3.title))
        self.assertEqual(updated_entry.content, "")

    # Test to see if logged out user is redirected to login page
    def test_redirect_to_login(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/")
