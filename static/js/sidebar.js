// Sidebar Toggle Script
function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    if (sidebar.style.left === "0px") {
        sidebar.style.left = "-250px"; // Close sidebar
    } else {
        sidebar.style.left = "0px"; // Open sidebar
    }
}
