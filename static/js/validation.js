document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("registrationForm").addEventListener("submit", function(event) {
        let inputs = document.querySelectorAll("input[name='studentName']");
        let phoneNumbers = document.querySelectorAll("input[name='phoneNumber']");
        
        for (let input of inputs) {
            if (!/^[A-Za-z ]+$/.test(input.value)) {
                alert("Student Name must contain only alphabets.");
                event.preventDefault();
                return;
            }
        }

        for (let phone of phoneNumbers) {
            if (!/^\d{10}$/.test(phone.value)) {
                alert("Phone Number must be exactly 10 digits.");
                event.preventDefault();
                return;
            }
        }
    });
});
