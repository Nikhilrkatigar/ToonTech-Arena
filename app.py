from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient

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

@app.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

@app.route('/startup')
def startup():
    return render_template('startup.html')

@app.route("/register", methods=["POST"])
def submit_registration():
    try:
        data = request.get_json()  # ✅ Ensure JSON format

        if not isinstance(data, list):  # ✅ Ensure data is a list
            return jsonify({"message": "Invalid data format"}), 400

        if len(data) == 0:
            return jsonify({"message": "No data received"}), 400

        user_id = "user1"  # ✅ Replace this with a real user ID if needed

        # Track duplicate events
        event_counts = {}

        cleaned_data = []
        for entry in data:
            event_name = entry.get("event_name", "No Event")

            if event_name == "No Event":
                continue  

            if event_name in event_counts:
                event_counts[event_name] += 1
                entry["event_name"] = f"{event_name}_{event_counts[event_name]}"
            else:
                event_counts[event_name] = 1

            entry["user_id"] = user_id  # ✅ Use "user_id" instead of "_id"
            cleaned_data.append(entry)

        if cleaned_data:
            collection.insert_many(cleaned_data)

        return jsonify({"message": "Registration Successful!"}), 200  # ✅ Always return JSON

    except Exception as e:
        print(f"Error: {str(e)}")  # ✅ Show errors in Flask logs
        return jsonify({"message": "Server Error", "error": str(e)}), 500

