document.addEventListener("DOMContentLoaded", function () {
    console.log("Gamification System Loaded!");

    let userPoints = localStorage.getItem("userPoints") || 0;
    
    function updatePoints(points) {
        userPoints = parseInt(userPoints) + points;
        localStorage.setItem("userPoints", userPoints);
        document.querySelector("#userPoints").innerText = userPoints;
    }

    document.querySelector("#completeTask").addEventListener("click", function () {
        updatePoints(10);  // User gets 10 points for completing a task
    });
});
