# from package import Groq
# from package import os

# from groq import Groq
# client = Groq(api_key="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")
# class Answer_Question_From_Documents:
#     def __init__(self,question : str, documents : list[str]) -> None:
#         self.question = question
#         self.documents = documents

#     def run(self) :
#         context = "\n".join(self.documents)  # Tạo chuỗi context bên ngoài f-string
#         input_text = f"""Question: {self.question}
#         Context: {context}
#         Answer:"""
#         completion = client.chat.completions.create(
#             model="llama3-70b-8192",
#             messages=[
#                 {"role": "system", 
#                  "content": "Bạn luôn phải trả lời bằng tiếng Việt, không dùng tiếng Anh."
#                 },
#                 {
#                     "role": "user",
#                     "content": self.question
#                 },
#                 {
#                     "role": "assistant",
#                     "content": input_text
#                 }
#             ],
#             temperature=1,
#             max_tokens=1024,
#             top_p=1,
#             stream=False,
#             stop=None,
#         )
#         return completion.choices[0].message.content
from groq import Groq

client = Groq(api_key="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")

class Answer_Question_From_Documents:
    def __init__(self, question: str, documents: list[str]) -> None:
        self.question = question
        self.documents = documents

    def run(self):
        context = "\n".join(self.documents)
        prompt = f"""Dựa vào thông tin sau, hãy trả lời câu hỏi bằng tiếng Việt tự nhiên.

        Thông tin:
        {context}
        
        Câu hỏi:
        {self.question}
        
        Trả lời:"""

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là một trợ lý thông minh, hãy nhớ luôn trả lời bằng Tiếng Việt."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1.0,
            stream=False,
            stop=None,
        )

        return completion.choices[0].message.content
