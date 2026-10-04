import sys
from fastapi import FastAPI
from flask import Flask, request
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

app = FastAPI()
flask_app = Flask(__name__)
client = OpenAI()
anthropic = __import__("anthropic").Anthropic()

SYSTEM = "You are a careful assistant. Answer only from the provided documents."


@app.post("/chat")
def chat(persona: str, question: str):
    messages = [
        # ruleid: user-input-in-system-prompt
        {"role": "system", "content": f"You are {persona}. Follow the user's rules."},
        # ok: user-input-in-system-prompt
        {"role": "user", "content": question},
    ]
    return client.chat.completions.create(model="model-name", messages=messages)


@app.post("/chat2")
async def chat2(question: str, tone: str):
    return anthropic.messages.create(
        model="model-name",
        max_tokens=256,
        # ruleid: user-input-in-system-prompt
        system="Reply in a {} tone".format(tone),
        messages=[{"role": "user", "content": question}],
    )


@flask_app.route("/ask", methods=["POST"])
def ask():
    body = request.get_json()
    # ruleid: user-input-in-system-prompt
    prompt = ChatPromptTemplate.from_messages([("system", "You help " + body["company"]), ("human", "{q}")])
    return prompt


def cli():
    role = sys.argv[1]
    # ruleid: user-input-in-system-prompt
    msg = SystemMessage(content=f"You are a {role}")
    return msg


def repl():
    name = input("Who are you? ")
    # ruleid: user-input-in-system-prompt
    return client.responses.create(model="model-name", instructions=f"The user is {name}", input="hi")


@app.post("/ok")
def ok_static_system(question: str):
    messages = [
        # ok: user-input-in-system-prompt
        {"role": "system", "content": SYSTEM},
        # ok: user-input-in-system-prompt
        {"role": "user", "content": question},
    ]
    return client.chat.completions.create(model="model-name", messages=messages)


@app.post("/ok2")
def ok_template_variable(question: str):
    # ok: user-input-in-system-prompt
    prompt = ChatPromptTemplate.from_messages([("system", "You answer questions about {topic}."), ("human", "{q}")])
    return prompt.invoke({"topic": "billing", "q": question})


@app.post("/ok3")
def ok_numeric(max_words: int, question: str):
    limit = int(max_words)
    # ok: user-input-in-system-prompt
    return anthropic.messages.create(model="model-name", max_tokens=256, system=f"Answer in at most {limit} words", messages=[{"role": "user", "content": question}])


def ok_config_not_user(settings):
    # ok: user-input-in-system-prompt
    return SystemMessage(content=f"Today is {settings.today}. Company: {settings.company}")
