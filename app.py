import os
import json
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from package import Sematic_search
from package import SentenceTransformer
from package import Answer_Question_From_Documents
from package import GoogleTranslator
from package import detect,LangDetectException
from package import GoogleTranslator
from package import Read_File_CSV

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sunlit-ace-441104-d6-4d4e430d2ff0.json"

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

list_chat_history = []

# st.title('Chatbot hỏi đáp các câu hỏi liên quan đến mô hình đảo Trường Sa lớn')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Bạn muốn tìm hiểu điều gì về quần đảo Trường Sa?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sidebar to display chat history
with st.sidebar:
    st.header("Lịch sử trò chuyện")
    for message in st.session_state.messages:
        if (message['role'].capitalize() == "User"):
            title = "Câu hỏi: " + message['content'] 
            st.write(title)

# Function for generating LLM response
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
            answer = GoogleTranslator(source='auto', target='vi').translate(title)
     
        return "Lỗi: {}".format(title)

def text_to_speech(text):
    tts = gTTS(text=text, lang="vi")
    tts.save("response.mp3")
    
    # Hiển thị trình phát âm thanh trong giao diện Streamlit
    st.audio("response.mp3", format="audio/mp3")

# Function to recognize speech using Google Speech-to-Text
def recognize_speech():
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            st.info("Đang lắng nghe, vui lòng nói...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="vi-VN")
            return text
        except sr.UnknownValueError:
            return "Không nhận diện được giọng nói. Hãy thử lại."
        except sr.RequestError:
            return "Lỗi kết nối khi nhận diện giọng nói. Hãy thử lại."
    
    except ZeroDivisionError as e:
        title = e
        if detect(title) != 'vi':
            answer = GoogleTranslator(source='auto', target='vi').translate(title)
        return "Lỗi: {}".format(title)
        
def is_vietnamese(text):
    if not text or len(text.strip()) < 5:  # có thể điều chỉnh ngưỡng tuỳ trường hợp
        return False
    try:
        return detect(text) == 'vi'
    except LangDetectException:
        return False

# Voice input button
# if st.button("🎙️ Thu giọng nói"):
#     try:
#         recognized_text = recognize_speech()
#         recognized_text = recognized_text.replace(".", "?")
#         if (recognized_text[-1] != '?'):
#             if (recognized_text[-1] == '.'):
#                 recognized_text[-1] = '?'
#             else:
#                 recognized_text += '?'
    
#         if recognized_text:
#             st.session_state.messages.append({"role": "user", "content": recognized_text})
#             # Save chat history after receiving the answer
            
    
#         with st.chat_message("user"):
#             st.write(recognized_text)
    
    
#         # Generate a response if last message is not from assistant
#         if st.session_state.messages[-1]["role"] != "assistant":
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     ans = generate_response(recognized_text)
#                     st.write(ans)
#                     message1 = {"role": "assistant", "content": ans}
#                     st.session_state.messages.append(message1)
#             with st.chat_message("assistant"):
#                 st.write("Chuyển hóa văn bản thành giọng nói?")
#                 text_to_speech(ans)
                
#     except ZeroDivisionError as e:
        
#         title = e
#         if detect(title) != 'vi':
#             answer = GoogleTranslator(source='auto', target='vi').translate(title)
        
#         with st.chat_message("assistant"):    
#             st.write("Lỗi: {}".format(title))
        
# User-provided prompt
if prompt := st.chat_input():
    try:
        prompt = prompt.replace(".", "?")
        if (prompt[-1] != '?'):
            if (prompt[-1] == '.'):
                prompt[-1] = '?'
            else:
                prompt += '?'
    
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        with st.chat_message("user"):
            st.write(prompt)
    
        # Generate a response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt)
                    st.write(response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message)
            # with st.chat_message("assistant"):
            #     text_to_speech(response)
            #     if os.path.exists("response.mp3"):
            #         if st.button("▶️ Nghe câu trả lời"):
            #             st.audio("response.mp3", format="audio/mp3")
                        
    except ZeroDivisionError as e:

        title = e
        if detect(title) != 'vi':
            answer = GoogleTranslator(source='auto', target='vi').translate(title)

        with st.chat_message("assistant"):    
            st.write("Lỗi: {}".format(title))
        # with st.chat_message("assistant"):
        #     st.write("Chuyển hóa văn bản thành giọng nói?")
        #     text_to_speech(response)


