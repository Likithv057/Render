document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const rentValue = document.getElementById('rent-value');

    // Initial value ₹0.00 on page load
    rentValue.innerText = '0.00';

    // Handle form submission with AJAX
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting in the traditional way

        const formData = new FormData(form);

        // Send form data to the Flask to fetch result
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Update the rent pridection result
            rentValue.innerText = data.predicted_rent.toFixed(2);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Reseting the rent value to ₹0.00 on reset 
    document.getElementById('resetButton').addEventListener('click', function() {
        rentValue.innerText = '0.00';
    });
});
