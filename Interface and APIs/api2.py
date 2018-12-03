#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS

app = Flask(__name__, static_url_path = "")
CORS(app)

dummy = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/dummy', methods = ['GET'])
def get_task():
    return jsonify( dummy[0] )

if __name__ == '__main__':
    app.run(debug = True)
