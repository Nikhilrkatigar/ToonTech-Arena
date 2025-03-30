document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded!");

    // ✅ Sidebar Toggle Function
    window.toggleSidebar = function () {
        var sidebar = document.getElementById("sidebar");
        sidebar.style.left = (sidebar.style.left === "-250px") ? "0" : "-250px";
    };

  

  // ✅ Dark Mode Toggle Fix
  const darkModeToggle = document.getElementById("darkModeToggle");
  if (!darkModeToggle) {
      console.warn("⚠ Dark Mode Toggle button not found!");
      return;  // Exit if the button is missing
  }

  const body = document.body;

  // Load saved dark mode preference
  if (localStorage.getItem("darkMode") === "enabled") {
      body.classList.add("dark-mode");
      darkModeToggle.textContent = "☀ Light Mode";
  }

  // ✅ Attach Dark Mode Toggle Event
  darkModeToggle.addEventListener("click", function () {
      body.classList.toggle("dark-mode");
      if (body.classList.contains("dark-mode")) {
          localStorage.setItem("darkMode", "enabled");
          darkModeToggle.textContent = "☀ Light Mode";
      } else {
          localStorage.setItem("darkMode", "disabled");
          darkModeToggle.textContent = "🌙 Dark Mode";
      }
  });
});

// ✅ jQuery Chat Functionality
$(document).ready(function () {
    if (typeof io === "undefined") {
        console.error("Socket.IO not loaded!");
        return;
    }

    var socket = io.connect(window.location.origin);

    // ✅ Load Chat Messages
    $.get('/get_messages', function (data) {
        if (data.messages) {
            data.messages.forEach(msg => {
                $('#message-list').append(`<li>${msg.text} <button onclick="deleteMessage('${msg.text}')">X</button></li>`);
            });
        }
    });

    // ✅ Send Message via WebSocket
    window.sendMessage = function () {
        let text = $('#message').val();
        if (text) {
            socket.emit('send_message', { text: text });
            $('#message').val('');
        }
    };

    // ✅ Receive Messages in Real-Time
    socket.on('receive_message', function (data) {
        $('#message-list').append(`<li>${data.text} <button onclick="deleteMessage('${data.text}')">X</button></li>`);
    });

    // ✅ Delete Message
    window.deleteMessage = function (text) {
        $.ajax({
            url: '/delete_message',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ text: text }),
            success: function () {
                location.reload();
            }
        });
    };

    // ✅ Attach Send Button Click Event
    $('.send-btn').click(sendMessage);
});
