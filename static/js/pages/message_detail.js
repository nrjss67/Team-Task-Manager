document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('textarea').addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.keyCode === 13) {
            e.preventDefault();
            this.form.submit();
        }
    });

    document.getElementById('cancelReply').addEventListener('click', function() {
        document.querySelector('form').reset();
    });
});