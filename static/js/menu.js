document.addEventListener("DOMContentLoaded", function () {
    console.log("Menu Loaded!");

    let menuBtn = document.querySelector(".menu-btn");
    let mobileMenu = document.querySelector(".mobile-menu");

    menuBtn.addEventListener("click", function () {
        mobileMenu.classList.toggle("show");
    });

    function toggleSidebar() {
        var sidebar = document.getElementById("sidebar");
        if (sidebar.style.left === "-250px") {
            sidebar.style.left = "0";
        } else {
            sidebar.style.left = "-250px";
        }
    }
});
