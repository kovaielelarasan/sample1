from flask import Flask, render_template, request, jsonify, url_for
import json
import random
import os

app = Flask(__name__)  # Required for Render + Gunicorn

# Path to static image directory
pic_folder = os.path.join('static', 'header')
app.config['UPLOAD_FOLDER'] = pic_folder

# Load chatbot Q&A data from static folder
with open(os.path.join('static', 'qa_data.json'), 'r') as file:
    intents = json.load(file)

# Home route → Registration page
@app.route('/')
def registration():
    return render_template('register.html')

# Function to get response from chatbot logic
def get_bot_response(user_input):
    user_input = user_input.lower()

    for intent in intents['intents']:
        if 'patterns' in intent and 'responses' in intent:
            for pattern in intent['patterns']:
                if pattern.lower() in user_input:
                    return random.choice(intent['responses'])

    return "I'm sorry, I don't understand that."

# Main chatbot route
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Static image URLs
    images = {
        'logo': url_for('static', filename='header/cc.jpg'),
        'name': url_for('static', filename='header/nam.jpg'),
        'banner': url_for('static', filename='header/aa.jpg'),
        'about': url_for('static', filename='header/about.jpg'),
        'icon1': url_for('static', filename='header/icon-1.png'),
        'icon2': url_for('static', filename='header/icon-2.png'),
        'icon3': url_for('static', filename='header/icon-3.png'),
        'gif': url_for('static', filename='header/vutura-chatbot.gif'),
        'why': url_for('static', filename='header/why-GRD-image.jpg'),
        'isro': url_for('static', filename='header/ISRO.jpg'),
        'national': url_for('static', filename='header/National-Symposium.png'),
    }
    return render_template("index.html", **images)

# API endpoint for chatbot
@app.route('/get_bot_response', methods=['POST'])
def get_bot_response_route():
    user_input = request.form.get('user_input')
    bot_response = get_bot_response(user_input)
    return jsonify({'bot_response': bot_response})

# Optional: manual launch for local testing
if __name__ == '__main__':
    app.run(debug=True)
