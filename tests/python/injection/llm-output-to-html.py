import bleach
import streamlit as st
from fastapi.responses import HTMLResponse
from flask import render_template_string
from markupsafe import Markup
from openai import OpenAI

client = OpenAI()


def chat_page(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    answer = resp.choices[0].message.content
    # ruleid: llm-output-to-html
    return Markup("<div class='answer'>" + answer + "</div>")


def fastapi_route(question: str):
    resp = client.responses.create(model="model-name", input=question)
    # ruleid: llm-output-to-html
    return HTMLResponse(content=f"<pre>{resp.output_text}</pre>")


def flask_route(chain, question: str):
    answer = chain.invoke({"question": question})
    # ruleid: llm-output-to-html
    return render_template_string("<p>" + answer + "</p>")


def streamlit_app(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    # ruleid: llm-output-to-html
    st.markdown(resp.choices[0].message.content, unsafe_allow_html=True)
    # ok: llm-output-to-html
    st.markdown(resp.choices[0].message.content)
    # ok: llm-output-to-html
    st.write(resp.choices[0].message.content)


def ok_sanitised(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    clean = bleach.clean(resp.choices[0].message.content, tags=["p", "b", "i", "code"])
    # ok: llm-output-to-html
    return Markup(clean)


def ok_template_autoescape(question: str):
    from flask import render_template
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    # ok: llm-output-to-html
    return render_template("answer.html", answer=resp.choices[0].message.content)
