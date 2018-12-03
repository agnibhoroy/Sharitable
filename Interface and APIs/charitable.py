#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import sqlite3

import paypal
import deposit_algorithm
import db

conn = db.connectDatabase('charitable.db')
app = Flask(__name__, static_url_path = "")
CORS(app)

def create_table():
    db.execute(conn, '''CREATE TABLE user_payments (userid integer, date text, amount integer)''')
    db.execute(conn, '''CREATE TABLE save_history (userid integer, date text, amount integer)''')
    #db.execute(conn, '''CREATE TABLE recommendations (userid integer, date text, amount integer)''')

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )

# User Payments Functions
@app.route('/charitable/user_pay/<userid>/<date>/<amount>', methods = ['GET'])
def set_userpay(userid, date, amount):
    db.execute(conn, 'INSERT INTO user_payments (userid, date, amount) VALUES (\"{}\", \"{}\", \"{}\")'.format(userid, date, amount))

    return jsonify( { 'task': [] } )

@app.route('/charitable/user_pay/<userid>', methods = ['GET'])
def get_userpay(userid):
    hello = db.execute(conn, 'SELECT date, amount FROM user_payments WHERE userid = {}'.format(userid)).fetchall()
    print(hello)

    output = []

    for hell in hello:
        output.append(list(hell))

    return jsonify( { 'out': output } )

# Save History Functions
@app.route('/charitable/save_hist/<userid>/<date>/<amount>', methods = ['GET'])
def set_savehist(userid, date, amount):
    db.execute(conn, 'INSERT INTO save_history (userid, date, amount) VALUES (\"{}\", \"{}\", \"{}\")'.format(userid, date, amount))

    return jsonify( { 'task': [] } )

@app.route('/charitable/save_hist/<userid>', methods = ['GET'])
def get_savehist(userid):
    hello = db.execute(conn, 'SELECT date, amount FROM save_history WHERE userid = {}'.format(userid)).fetchall()
    print(hello)
    output = []

    for hell in hello:
        output.append(list(hell))

    return jsonify( { 'out': output } )

@app.route('/charitable/paypal/<userid>/<date>/<amount>', methods = ['GET'])
def process_payment(userid, date, amount):
    payment = paypal.define_payment(amount, userid, date)
    paypal.create_payment(payment)
    output = paypal.execute_payment(payment)

    if output == 'success':
        return jsonify( { 'out': 'success' } )
    else:
        return jsonify( { 'out': 'failure' } )

@app.route('/charitable/paypal/<userid>', methods = ['GET'])
def generate_instructions(userid):
    instructions = deposit_algorithm.output(userid)

    output = {
        'deposit': instructions[0],
        'suggestions': instructions[1]
    }

    return jsonify(output)

if __name__ == '__main__':
    #create_table()
    app.run(debug = True)
