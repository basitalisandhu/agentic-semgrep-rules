import httpx
import requests
import urllib.request
from openai import OpenAI

client = OpenAI()


def browse_tool(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    url = resp.choices[0].message.content
    # ruleid: llm-output-to-http-request
    page = requests.get(url, timeout=10)
    # ruleid: llm-output-to-http-request
    httpx.post(url=url, json={})
    # ruleid: llm-output-to-http-request
    urllib.request.urlopen(url)
    return page.text


def session_fetch(task: str):
    resp = client.responses.create(model="model-name", input=task)
    session = requests.Session()
    # ruleid: llm-output-to-http-request
    return session.get(resp.output_text + "/api")


def langchain_loader(chain, question: str):
    from langchain_community.document_loaders import WebBaseLoader
    url = chain.invoke({"question": question})
    # ruleid: llm-output-to-http-request
    return WebBaseLoader(url).load()


def ok_fixed_host_with_model_query(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    query = resp.choices[0].message.content
    # ok: llm-output-to-http-request
    return requests.get("https://api.example.com/search", params={"q": query}, timeout=10)


def ok_validated(task: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": task}])
    url = validate_url(resp.choices[0].message.content, allowed_hosts=["docs.example.com"])
    # ok: llm-output-to-http-request
    return requests.get(url, timeout=10, allow_redirects=False)


def ok_static():
    # ok: llm-output-to-http-request
    return requests.get("https://example.com/health", timeout=5)
