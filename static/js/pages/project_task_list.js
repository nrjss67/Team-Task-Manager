document.addEventListener('DOMContentLoaded', function() {
    // Select All Tasks
    const selectAllCheckbox = document.getElementById('selectAllTasks');
    const taskCheckboxes = document.querySelectorAll('tbody .form-check-input');

    selectAllCheckbox?.addEventListener('change', function() {
        taskCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });
});
