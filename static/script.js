document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded!"); // Keep this if needed

    // Create a glow effect div
    let cursorGlow = document.createElement("div");
    cursorGlow.classList.add("cursor-glow");
    document.body.appendChild(cursorGlow);

    document.addEventListener("mousemove", function (e) {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });
});
