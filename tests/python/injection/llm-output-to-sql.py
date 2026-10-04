import sqlite3
from sqlalchemy import text
from openai import OpenAI

client = OpenAI()
conn = sqlite3.connect("app.db")


def text_to_sql(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    sql = resp.choices[0].message.content
    cur = conn.cursor()
    # ruleid: llm-output-to-sql
    cur.execute(sql)
    # ruleid: llm-output-to-sql
    cur.executescript("BEGIN; " + sql + "; COMMIT;")
    return cur.fetchall()


def interpolated(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    name = resp.choices[0].message.content
    cur = conn.cursor()
    # ruleid: llm-output-to-sql
    cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
    # ruleid: llm-output-to-sql
    cur.execute("SELECT * FROM users WHERE name = '%s'" % name)


def sqlalchemy_text(engine, chain, question: str):
    generated = chain.invoke({"question": question})
    with engine.connect() as c:
        # ruleid: llm-output-to-sql
        c.execute(text(generated))


def pandas_query(engine, agent, question: str):
    import pandas as pd
    query = agent.run(question)
    # ruleid: llm-output-to-sql
    return pd.read_sql(query, engine)


def ok_parameterised(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    name = resp.choices[0].message.content
    cur = conn.cursor()
    # ok: llm-output-to-sql
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    # ok: llm-output-to-sql
    cur.execute("SELECT * FROM users WHERE name = :name", {"name": name})


def ok_numeric_cast(question: str):
    resp = client.chat.completions.create(model="model-name", messages=[{"role": "user", "content": question}])
    limit = int(resp.choices[0].message.content)
    cur = conn.cursor()
    # ok: llm-output-to-sql
    cur.execute(f"SELECT * FROM users LIMIT {limit}")


def ok_static():
    cur = conn.cursor()
    # ok: llm-output-to-sql
    cur.execute("SELECT 1")
