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
    data = request.json  # Get JSON data from frontend

    if not isinstance(data, list):  # Ensure data is a list
        return jsonify({"message": "Invalid data format"}), 400

    if len(data) == 0:
        return jsonify({"message": "No data received"}), 400

    # Assign a user ID (you can generate unique IDs based on session/auth)
    user_id = "user1"  # Replace with dynamic user IDs if needed

    # Dictionary to track duplicate events
    event_counts = {}

    # Modify event names before inserting into MongoDB
    for entry in data:
        event_name = entry["event_name"]

        # Remove "No Event" and name duplicate events properly
        if event_name == "No Event":
            continue  # Skip No Event entries

        if event_name in event_counts:
            event_counts[event_name] += 1
            entry["event_name"] = f"{event_name}_{event_counts[event_name]}"
        else:
            event_counts[event_name] = 1

        entry["_id"] = user_id  # Assign user_id to each entry

    collection.insert_many(data)  # Store entries in MongoDB
    return jsonify({"message": "Registration Successful!"})
