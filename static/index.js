// Wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get references to the form and button
  const form = document.getElementById("form");
  const button = document.getElementById("btn_internet");

  // Add click event listener to the button
  button.addEventListener("click", function() {
    // Toggle the visibility of the form
    if (form.style.display === "none") {
      form.style.display = "block"; // Show the form
}  
});
});
