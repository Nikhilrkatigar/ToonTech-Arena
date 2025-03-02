document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded!");

    // Menu Button Click Event
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

    // Cursor Glow Effect
    let cursorGlow = document.createElement("div");
    cursorGlow.classList.add("cursor-glow");
    document.body.appendChild(cursorGlow);

    document.addEventListener("mousemove", function (e) {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });
});
