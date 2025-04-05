from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from analysis import process_video

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    video_path = os.path.join('temp', file.filename)
    file.save(video_path)
    
    results = process_video(video_path)
    return jsonify(results)

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)