document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");
    const urlInput = document.getElementById("urlInput");
    // const backendUrl = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000' : 'https://whatthehack.vercel.app/?';
    const backendUrl = 'https://whatthehack.vercel.app';
    submitBtn.addEventListener("click", () => {
        const url = urlInput.value;
        if (url) {
            // Send URL to the server via a POST request
            fetch(`${backendUrl}/get_url`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }) // Send the URL as JSON
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server Response:", data);  // Check the response
                if (data.request_id) {
                    // Store the request ID in localStorage for polling
                    localStorage.setItem('request_id', data.request_id);
                    // Redirect to the loading page
                    window.location.href = "/loading";
                }
            })
            .catch(error => {
                alert("Error sending URL to server: " + error);
            });
        } else {
            alert("Please enter a valid URL.");
        }
    });

    // Poll the server for the processed result
    function checkProcessingStatus() {
        const requestId = localStorage.getItem('request_id');
        if (requestId) {
            fetch(`http://127.0.0.1:5000/get_processed_result/${requestId}`)
            .then(response => response.json())
            .then(data => {
                console.log("Polling response:", data);  // For debugging
                if (data.message === "Still processing...") {
                    console.log("Still processing...");
                    setTimeout(checkProcessingStatus, 1000); // Poll again after 1 second
                } else {
                    // If result is ready, redirect to the result page
                    console.log("Processing complete. Redirecting to result page.");
                    window.location.href = `/result/${requestId}`; // Redirect to result page
                }
            })
            .catch(error => {
                console.error("Error checking processing status:", error);
            });
        }
    }

    // Start polling if we're on the loading page
    if (window.location.pathname === '/loading') {
        checkProcessingStatus(); // Start polling when we are on the loading page
    }
});