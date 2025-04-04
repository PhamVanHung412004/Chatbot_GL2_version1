import os
import uuid
from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
from gtts import gTTS
from package import (
    Sematic_search,
    SentenceTransformer,
    Answer_Question_From_Documents,
    GoogleTranslator,
    Read_File_CSV
)
from langdetect import detect, LangDetectException

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model embedding một lần khi server start
model = SentenceTransformer("all-MiniLM-L6-v2")

# ====== Function chính ======
def generate_response(user_query):
    try:
        list_index = Sematic_search(model, user_query, 3).run()
        vector = [int(i) for i in list_index[0]]
        datas = Read_File_CSV("dataset.csv").run()
        list_context = [datas["text"][i] for i in vector]

        answer = Answer_Question_From_Documents(user_query, list_context).run()

        if detect(answer) != 'vi':
            answer = GoogleTranslator(source='auto', target='vi').translate(answer)

        return answer
    except Exception as e:
        message = str(e)
        if detect(message) != 'vi':
            message = GoogleTranslator(source='auto', target='vi').translate(message)
        return f"Lỗi: {message}"

def text_to_speech(text):
    tts = gTTS(text=text, lang="vi")
    path = os.path.join(app.config['UPLOAD_FOLDER'], "response.mp3")
    tts.save(path)
    return path

# ====== API routes ======

@app.route('/')
def index():
    return "Server is running. Use /api/query or /api/upload"

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Không có câu hỏi'}), 400

    answer = generate_response(query)
    return jsonify({'answer': answer})

@app.route('/api/speech-to-text', methods=['POST'])
def handle_speech_to_text():
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file'}), 400

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + ".wav")
    file.save(file_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="vi-VN")
            return jsonify({'text': text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def handle_text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Thiếu nội dung văn bản'}), 400

    path = text_to_speech(text)
    return send_file(path, mimetype='audio/mpeg', as_attachment=True, download_name="response.mp3")

# ====== Run app ======
if __name__ == '__main__':
    app.run(debug=True)
