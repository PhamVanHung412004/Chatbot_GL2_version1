import speech_recognition as sr
from gtts import gTTS
from package import Sematic_search
from package import SentenceTransformer
from package import Answer_Question_From_Documents
from package import GoogleTranslator
from package import detect,LangDetectException
from package import GoogleTranslator
from package import Read_File_CSV

import os
import uuid
from flask import Flask, flash, request, redirect


UPLOAD_FOLDER = 'files'

app = Flask(__name__)

# download model embedding
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# gen context
def generate_response(use_query):
    try:
        list_index = Sematic_search(load_model(), use_query,3).run()
        vector_tmp = list_index[0]
        vector = [int(i) for i in vector_tmp]
        datas = Read_File_CSV("dataset.csv").run()

        list_context = [datas["text"][i] for i in vector]
        answer = Answer_Question_From_Documents(use_query,list_context).run()

        # Kiểm tra nếu câu trả lời không phải tiếng Việt thì mới dịch
        if detect(answer) != 'vi':
            answer = GoogleTranslator(source='auto', target='vi').translate(answer)

        return answer

    except ZeroDivisionError as e:
        title = e
        if detect(title) != 'vi':
            title = GoogleTranslator(source='auto', target='vi').translate(title)
        
        return "Eror: {}".format(title)



    
    # Hiển thị trình phát âm thanh trong giao diện Streamlit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/save-record', methods=['POST'])
# def save_record():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     # if user does not select file, browser also
#     # submit an empty part without filename
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     file_name = str(uuid.uuid4()) + ".mp3"
#     full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
#     file.save(full_file_name)

# text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="vi")
    tts.save("response.mp3")
    return '<h1>Success</h1>'

# vocie
def recognize_speech():
    recognizer = sr.Recognizer()    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        return text
    except sr.UnknownValueError:
        return "Không nhận diện được giọng nói. Hãy thử lại."
    except sr.RequestError:
        return "Lỗi kết nối khi nhận diện giọng nói. Hãy thử lại."

def is_vietnamese(text):
    if not text or len(text.strip()) < 5:  # có thể điều chỉnh ngưỡng tuỳ trường hợp
        return False
    try:
        return detect(text) == 'vi'
    except LangDetectException:
        return False

if __name__ == '__main__':
    app.run()
