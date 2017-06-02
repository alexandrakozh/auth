from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import app.views

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)