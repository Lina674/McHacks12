document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");
    const urlInput = document.getElementById("urlInput");

    submitBtn.addEventListener("click", () => {
        const url = urlInput.value;

        if (url) {
            // Send URL to the server via a POST request
            fetch('http://127.0.0.1:5000/get_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }) // Send the URL as JSON
            })
            .then(response => response.json())
            .then(data => {
                // After successfully sending the URL, redirect to the loading page
                console.log("Server Response:", data);  // Add this to check the response
                window.location.href = "loading.html";
            })
            .catch(error => {
                alert("Error sending URL to server: " + error);
            });
        } else {
            alert("Please enter a valid URL.");
        }
    });
});
