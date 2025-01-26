document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");
    const urlInput = document.getElementById("urlInput");
    const backendUrl = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000' : 'https://whatthehack.vercel.app';

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
    function checkProcessingStatus(startTime) {
        const requestId = localStorage.getItem('request_id');
        const maxPollingTime = 8000;  // Timeout after 8 seconds (8000 ms)

        if (requestId) {
            // Check the elapsed time
            const elapsedTime = Date.now() - startTime;

            if (elapsedTime < maxPollingTime) {
                fetch(`${backendUrl}/get_processed_result/${requestId}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Polling response:", data);  // For debugging
                        if (data.message === "Still processing...") {
                            console.log("Still processing...");
                            setTimeout(() => checkProcessingStatus(startTime), 1000); // Poll again after 1 second
                        } else {
                            // If result is ready, redirect to the result page
                            console.log("Processing complete. Redirecting to result page.");
                            window.location.href = `/result/${requestId}`; // Redirect to result page
                        }
                    })
                    .catch(error => {
                        console.error("Error checking processing status:", error);
                    });
            } else {
                // Timeout reached, handle accordingly
                console.log("Timeout reached. No result yet.");
                alert("Processing timed out. Please try again later.");
                window.location.href = "/"; // Redirect to home or any other appropriate action
            }
        }
    }

    // Start polling if we're on the loading page
    if (window.location.pathname === '/loading') {
        const startTime = Date.now();  // Store the time when polling starts
        checkProcessingStatus(startTime); // Start polling when we are on the loading page
    }
});
