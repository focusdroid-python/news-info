

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/info'
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask


app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True)