function validateForm() {

    var email = document.getElementById('{{ form.name.id_for_label }}').value;

    var emailRegex = /^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/;
    if (email.length === 0 || !emailRegex.test(email)) {
        alert("Email address must be in the format of 'name@domain.extension'. Please enter a valid email address.");
        return false;
    }

    var selectedBlockId = document.getElementById('selected_block_id').value;
    if (selectedBlockId) {
        var form = document.querySelector('.form-container');
        form.action = "/" + selectedBlockId + "/"; // URL'i güncelle
        form.submit(); // Formu gönder
    } else {
        alert("You must select the block first.");
        return false;
    }

    return true; // Tüm kontrollerden geçerse formu gönder
}
