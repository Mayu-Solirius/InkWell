$(document).ready(function () {
    function saveEntry(entryId, title, content) {
        $.ajax({
            url: '{% url "save_journal_entry" %}',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'entry_id': entryId,
                'title': title,
                'content': content,
            },
            success: function (response) {
                if (response.status === 'success') {
                    console.log('Entry saved successfully.');
                } else {
                    console.error('Error saving entry:', response.errors);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error saving entry:', error);
            },
        });
    }

    $('.journal-entry').on('click', function () {
        const entryId = $(this).data('entry-id');
        const titleField = $(this).find('.entry-title');
        const contentField = $(this).find('.entry-content');

        // Remove readonly attribute on click to enable editing
        titleField.removeAttr('readonly');
        contentField.removeAttr('readonly');

        // Save changes when the user clicks outside the field
        $(document).on('blur', '.entry-title, .entry-content', function () {
            const entryId = $(this).parent().data('entry-id');
            const title = titleField.val();
            const content = contentField.val();

            saveEntry(entryId, title, content);
        });
    });
});