document.addEventListener('DOMContentLoaded', function() {
    // Базові елементи
    const selectAllBtn = document.getElementById('selectAll');
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    const messageCheckboxes = document.querySelectorAll('input[name="message_ids[]"]');
    const archiveButton = document.getElementById('archiveSelected');
    const deleteButton = document.getElementById('deleteSelected');

    let selectedIds = []; // Масив для зберігання вибраних ID

    // Оновлення стану кнопок та списку ID
    function updateSelection() {
        selectedIds = Array.from(document.querySelectorAll('input[name="message_ids[]"]:checked'))
            .map(checkbox => checkbox.value);
        
        // Оновлюємо стан кнопок
        archiveButton.disabled = selectedIds.length === 0;
        deleteButton.disabled = selectedIds.length === 0;
        
        console.log('Selected IDs:', selectedIds); // Для дебагу
    }

    // Select All
    selectAllBtn?.addEventListener('click', function() {
        const isChecked = selectAllCheckbox.checked;
        selectAllCheckbox.checked = !isChecked;
        messageCheckboxes.forEach(checkbox => {
            checkbox.checked = !isChecked;
        });
        updateSelection();
    });

    // Окремі чекбокси
    messageCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function(e) {
            e.stopPropagation();
            updateSelection();
        });
    });

    // Функція для відправки POST запиту
    function submitAction(action) {
        if (selectedIds.length === 0) return;
        
        const formData = new FormData();
        formData.append('action', action);
        selectedIds.forEach(id => formData.append('message_ids[]', id));

        fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Archive button
    archiveButton?.addEventListener('click', function() {
        submitAction('archive');
    });

    // Delete button
    deleteButton?.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete selected messages?')) {
            submitAction('delete');
        }
    });

    // Початковий стан
    updateSelection();
});
