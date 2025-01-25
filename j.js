document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");
    const urlInput = document.getElementById("urlInput");

    submitBtn.addEventListener("click", () => {
        const url = urlInput.value;

        if (url) {
            // Store URL in localStorage to use it on the loading page
            localStorage.setItem("url", url);

            // Redirect to the loading page
            window.location.href = "loading.html";
        } else {
            alert("Please enter a valid URL.");
        }
    });
});
