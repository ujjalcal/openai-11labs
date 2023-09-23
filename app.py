from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)  # To handle CORS

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_audio_response', methods=['POST'])
def get_audio_response():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file received."}), 400

    file = request.files['audio']

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Here, process the audio with your chatbot.
        # Since you mentioned your server API knows how to create a transcript from voice,
        # you would process it accordingly. For now, I'm just returning a stub message.

        return jsonify({"response": "Processed your audio."})
    
    return jsonify({"error": "File format not supported."}), 400

@app.route('/get_response', methods=['POST'])
def get_response():
    typed_message = request.form.get('typed_message')
    # Process the typed_message with your chatbot.
    # For this example, let's just return a reversed version of the typed_message.
    response = typed_message[::-1]
    return jsonify({"response": response})

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)  # Create uploads folder if it doesn't exist
    app.run(debug=True)
