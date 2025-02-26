from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__, template_folder="templates")  # Ensure Flask finds HTML files
CORS(app)

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

# ✅ Registration API (for form submission)
@app.route("/register", methods=["POST"])
def submit_registration():
    data = request.json  # Get JSON data from frontend

    if not isinstance(data, list):  # Ensure data is a list
        return jsonify({"message": "Invalid data format"}), 400

    if len(data) == 0:
        return jsonify({"message": "No data received"}), 400

    collection.insert_many(data)  # Store multiple entries in MongoDB

    return jsonify({"message": "Registration Successful!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
