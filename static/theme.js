// theme.js
document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    function toggleTheme() {
        body.classList.toggle('dark-theme');
    
        const isDarkTheme = body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDarkTheme ? 'dark' : 'light');
    }
    
    themeToggle.addEventListener("click", toggleTheme);
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
    }
});


function showExportingMessage() {
    // Display a message indicating that exporting is in progress
    alert("Exporting songs... Please wait.");
}

function showExportSuccessMessage() {
    // Display a success message after exporting is complete
    alert("All songs have been exported!");
}

function showExportErrorMessage() {
    // Display an error message if exporting fails
    alert("Export failed!");
}

