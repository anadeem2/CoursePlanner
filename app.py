from flask import Flask
from cs50 import SQL
import pyodbc

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)