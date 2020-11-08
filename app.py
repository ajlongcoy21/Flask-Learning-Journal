# source ./env/bin/activate
# deactivate

from flask import Flask

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    
    app.run(debug=DEBUG, host=HOST, port=PORT)