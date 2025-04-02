from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from flask_socketio import SocketIO

import os

# ✅ Initialize Flask and SocketIO
app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

# ✅ Connect to MongoDB
client = MongoClient("mongodb+srv://nikhilkatigar76:Nikhil%407996@toontecharena.9eh6h.mongodb.net/?retryWrites=true&w=majority")
db = client["toontech_arena"]
collection = db["registrations"]
chat_collection = db["messages"]  # Chat messages collection

MAX_MESSAGES = 400  # Maximum number of messages to keep in memory

# ✅ Home Page
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Event Pages
@app.route('/coding')
def coding():
    return render_template('coding.html')

@app.route('/communication')
def communication():
    return render_template('communication.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/gaming')
def gaming():
    return render_template('gaming.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/startup')
def startup():
    return render_template('startup.html')

# ✅ Registration Pages
@app.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

@app.route('/register_bba', methods=['GET'])
def show_bba_register_page():
    return render_template('bba_registration.html')

# ✅ Chat Page
@app.route('/chat')
def show_chat_page():
    return render_template('chat.html')

# ✅ API to fetch messages from MongoDB
@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = list(chat_collection.find({}, {"_id": 0, "text": 1}))  
    return jsonify({"messages": messages[-MAX_MESSAGES:]})  

# ✅ API to send a message (Fixed variable issue)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Message text required"}), 400

    message_text = data["text"]

    # ✅ Store message in MongoDB
    chat_collection.insert_one({"text": message_text})

    return jsonify({"success": True, "message": "Message sent successfully!"})

# ✅ WebSocket: Handle sending messages
@socketio.on('send_message')
def handle_send_message(data):
    message_text = data.get("text")
    
    if message_text:
        chat_collection.insert_one({"text": message_text})  # Store in MongoDB
        socketio.emit('receive_message', {"text": message_text}, broadcast=True)  # Broadcast message

# ✅ API to delete a message
@app.route('/delete_message', methods=['POST'])
def delete_message():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "No message provided"}), 400

    chat_collection.delete_one({"text": data["text"]})
    return jsonify({"status": "Message deleted successfully!"}), 200

# ✅ Registration API for B.C.A
@app.route("/register", methods=["POST"])
def submit_registration():
    try:
        data = request.get_json()
        if not isinstance(data, list) or len(data) == 0:
            return jsonify({"message": "Invalid or empty data"}), 400

        course_type = data[0].get("course_type", "Unknown")
        event_counts = {}
        cleaned_data = []

        for entry in data:
            event_name = entry.get("event_name", "").strip()
            if not event_name:
                continue  

            if event_name in event_counts:
                event_counts[event_name] += 1
                entry["event_name"] = f"{event_name}_{event_counts[event_name]}"
            else:
                event_counts[event_name] = 1

            entry["user_id"] = "user1"
            entry["course_type"] = course_type
            cleaned_data.append(entry)

        if cleaned_data:
            collection.insert_many(cleaned_data)

        return jsonify({"message": f"{course_type} B.C.A Registration Successful!"}), 200

    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

# ✅ Registration API for B.B.A
@app.route("/register_bba", methods=["POST"])
def register_bba():
    try:
        student_name = request.form.getlist("student_name")
        phone_number = request.form.getlist("phone_number")
        register_number = request.form.getlist("register_number")
        class_name = request.form.getlist("class")

        event_names = ["Management", "Management 2", "Communication", "Data Analyzing", "Data Analyzing 2", "Gaming", "Financial", "Financial 2"]

        registrations = []
        for i in range(len(student_name)):
            event_name = event_names[i % len(event_names)]
            registrations.append({
                "event_name": event_name,
                "student_name": student_name[i],
                "phone_number": phone_number[i],
                "register_number": register_number[i],
                "class": class_name[i],
                "course_type": "BBA"
            })

        if registrations:
            collection.insert_many(registrations)

        return jsonify({"success": True, "message": "B.B.A Registration Successful!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Error occurred", "error": str(e)}), 500

# ✅ Start Flask & SocketIO
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=True, host="0.0.0.0", port=port)
