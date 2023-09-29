from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY 환경 변수를 설정해주세요.")

openai.api_key = api_key

@app.route("/translater", methods=["post"])
def translater():
    data = request.json
    language = data["language"]
    text = data["text"]

    prompt = f"If you ask questions in Korean, translate them into English and understand it in English. Make an English grammar problem with the type of {text}\n\n You are a globally capable English teacher. You made and published TOEIC workbooks for middle school, high school, and college students in Korea.Make an English question, make a split line at the bottom, Write down the correct answer in the beginning of the explanation.translate the explanation into Korean and write it in detail.Write down in detail why the correct answer is correct and why the wrong part is wrong.And make English questions without errors like English grammar experts. write ' {language} ',which is the content of this question"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "If you ask questions in Korean, translate them into English and understand it in English.You are an English grammar expert who makes TOEIC and TOEFL workbooks in Korea. And you are an English teacher who teaches high school students."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
    )
    return response["choices"][0]["message"]["content"]


@app.route("/web")
def web():
    return render_template("index.html")


@app.route("/")
def index():
    return "<a href='/web'>안녕하세요. 이곳은 영어 문제를 쓰는 사이트입니다. 클릭하면 사이트에 들어갑니다.</a>"
     
app.run(host="0.0.0.0", debug=True, port=3000)
