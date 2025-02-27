document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById("registrationForm");

    if (!form) {
        console.error("Form not found! Check if 'register.html' contains <form id='registrationForm'>.");
        return;
    }

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form from reloading the page

        let formDataArray = [];
        let rows = document.querySelectorAll(".table tr");

        rows.forEach((row, index) => {
            if (index === 0) return; // Skip the header row

            let eventName = row.cells[0].textContent.trim();
            let studentName = row.cells[1].querySelector("input").value.trim();
            let phoneNumber = row.cells[2].querySelector("input").value.trim();
            let registerNumber = row.cells[3].querySelector("input").value.trim();
            let className = row.cells[4].querySelector("input").value.trim();

            if (studentName && phoneNumber && registerNumber && className) {
                formDataArray.push({
                    event_name: eventName || "No Event", // Default if event name is empty
                    student_name: studentName,
                    phone_number: phoneNumber,
                    register_number: registerNumber,
                    class: className
                });
            }
        });

        if (formDataArray.length === 0) {
            alert("Please fill at least one row!");
            return;
        }

        // Send data to Flask backend
        fetch("https://toontech-arena.onrender.com/register", {  
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formDataArray)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show success message
            form.reset(); // Clear form after submission
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Registration failed. Please try again.");
        });
    });
});
