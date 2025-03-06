from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, template_folder="templates")  # Ensure Flask finds HTML files
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Connect to MongoDB
client = MongoClient("mongodb+srv://nikhilkatigar76:Nikhil%407996@toontecharena.9eh6h.mongodb.net/?retryWrites=true&w=majority")

db = client["toontech_arena"]
collection = db["registrations"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/coding')
def coding():
    return render_template('coding.html', title="Coding Event")

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

@app.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

@app.route('/startup')
def startup():
    return render_template('startup.html')

@app.route('/register_bba', methods=['GET'])
def show_bba_register_page():
    return render_template('bba_registration.html')

# ✅ Registration API for B.C.A
@app.route("/register", methods=["POST"])
def submit_registration():
    try:
        data = request.get_json()  # ✅ Ensure JSON format

        if not isinstance(data, list):  # ✅ Ensure data is a list
            return jsonify({"message": "Invalid data format"}), 400

        if len(data) == 0:
            return jsonify({"message": "No data received"}), 400

        # ✅ Extract Course Type (BCA or BBA)
        course_type = data[0].get("course_type", "Unknown")

        # ✅ Track duplicate events
        event_counts = {}

        cleaned_data = []
        for entry in data:
            event_name = entry.get("event_name", "").strip()

            # ✅ Skip empty event names
            if not event_name:
                continue  

            # ✅ Rename duplicate events (e.g., "Coding", "Coding_2")
            if event_name in event_counts:
                event_counts[event_name] += 1
                entry["event_name"] = f"{event_name}_{event_counts[event_name]}"
            else:
                event_counts[event_name] = 1

            entry["user_id"] = "user1"  # ✅ Use "user_id" instead of "_id"
            entry["course_type"] = course_type  # ✅ Store course type (BCA or BBA)
            cleaned_data.append(entry)

        if cleaned_data:
            collection.insert_many(cleaned_data)

        return jsonify({"message": f"{course_type} B.C.A Registration Successful!"}), 200  # ✅ Always return JSON

    except Exception as e:
        print(f"Error: {str(e)}")  # ✅ Show errors in Flask logs
        return jsonify({"message": "Server Error", "error": str(e)}), 500

# ✅ Registration API for B.B.A (Updated)
@app.route("/register_bba", methods=["GET", "POST"])
def register_bba():
    try:
        student_name = request.form.getlist("student_name")
        phone_number = request.form.getlist("phone_number")
        register_number = request.form.getlist("register_number")
        class_name = request.form.getlist("class")

        # ✅ Correct Event Names for B.B.A
        event_names = ["Management", "Management 2", "Communication", "Data Analyzing", "Data Analyzing 2", "Gaming", "Financial", "Financial 2"]

        registrations = []
        for i in range(len(student_name)):
            # ✅ Assign event names properly
            event_name = event_names[i % len(event_names)]  # Ensures correct mapping

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

        return jsonify({"success": True, "message": "B.B.A Registration Successful!"}), 200  # ✅ Return JSON response

    except Exception as e:
        return jsonify({"success": False, "message": "Error occurred", "error": str(e)}), 500  # ✅ Handle errors properly


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port
    app.run(debug=True, host="0.0.0.0", port=port)
