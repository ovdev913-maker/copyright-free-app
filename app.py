import os
from flask import Flask, request, send_file, jsonify
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Video Copyright Remover Backend is Running!"

@app.route('/process-video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file found"}), 400
        
    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "copyright_free_" + file.filename)
    file.save(input_path)

    try:
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', 'setpts=1.01*PTS,scale=1280:720',
            '-af', 'asetrate=44100*0.99,atempo=1.02',
            '-map_metadata', '-1',
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
