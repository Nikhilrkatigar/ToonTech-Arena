document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("bbaForm").addEventListener("submit", function (event) {
        let valid = true;
        const nameRegex = /^[A-Za-z\s]+$/;
        const phoneRegex = /^\d{10}$/;

        // Get all input fields
        let inputs = document.querySelectorAll("#bbaForm input");

        inputs.forEach(input => {
            let name = input.getAttribute("name");
            let value = input.value.trim();

            if (name === "student_name" && !nameRegex.test(value)) {
                alert("Student name should contain only alphabets.");
                valid = false;
            }

            if (name === "phone_number" && !phoneRegex.test(value)) {
                alert("Phone number should contain exactly 10 digits.");
                valid = false;
            }
        });

        if (!valid) {
            event.preventDefault();
        } else {
            let formData = new FormData(this);
            fetch("/register_bba", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // ✅ Show success or error message
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            });

            event.preventDefault(); // ✅ Prevent page reload after form submission
        }
    });
});
