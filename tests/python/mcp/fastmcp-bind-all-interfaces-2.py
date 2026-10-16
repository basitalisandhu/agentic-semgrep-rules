import uvicorn
from fastapi import FastAPI
from flask import Flask

app = FastAPI()
web = Flask(__name__)

if __name__ == "__main__":
    # ok: fastmcp-bind-all-interfaces
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # ok: fastmcp-bind-all-interfaces
    web.run(host="0.0.0.0", port=5000)
