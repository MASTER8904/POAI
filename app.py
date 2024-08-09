from flask import Flask, render_template, request, send_from_directory, jsonify
import sqlite3
import os
import bcrypt

app = Flask(__name__)
port = 3000

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/log')
def login_page():
    return send_from_directory('templates', 'login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    try:
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password, result[0]):
            return send_from_directory('templates', 'details.html')
        else:
            return jsonify({'message': 'Only Admins are allowed...'}), 401
    except Exception as e:
        print(f'Error connecting to SQLite or querying the database: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

@app.route('/details', methods=['POST'])
def get_student_details():
    regno = request.form['regno']

    try:
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name_of_the_student, company_employed, campus_status, batch FROM students WHERE roll_no=?", (regno,))
        result = cursor.fetchone()
        conn.close()

        if result:
            student_details = {
                'roll_no': result[0],
                'name': result[1],
                'company': result[2],
                'campus_status': result[3],
                'batch': result[4]
            }
            return jsonify({'student': student_details})

        else:
            return jsonify({'error': 'No student found with that registration number.'})
    except Exception as e:
        print(f'Error querying the database: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(port=port)
