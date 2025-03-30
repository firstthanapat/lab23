from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="db_server",
    user="root",
    password="rootpassword",
    database="unidb"
)

@app.route('/')
def hello():
    return "Hello from Flask Backend!"

@app.route('/api/users')
def get_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    users = cursor.fetchall()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Create requirements.txt inside ~/practice/app/
nano app/requirements.txt
Add Flask and MySQL Connector as dependencies:
Flask
mysql-connector-python

Create shell script inside ~/practice/app/
nano app/script.sh

#!/bin/sh
pip install -r requirements.txt
python app.py

Create docker compose inside ~/practice/
services:
  web:
    image: python:3.9
    ports:
      - "5000:5000"
    working_dir: /app
    volumes:
      - ./app:/app  # Mount a local directory for web data
    command: ["sh", "script.sh"]
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql
    container_name: db_server
    volumes:
      - ./db:/docker-entrypoint-initdb.d
    ports:
      - "3606:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 3
      start_period: 5s

