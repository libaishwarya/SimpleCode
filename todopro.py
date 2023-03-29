from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydatabase"
)


app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    mailID = data['mailID']
    passwords = data['passwords']
    cursor = mydb.cursor()
    sql = "INSERT INTO userDetails (name, mailID, passwords) VALUES (%s, %s, %s)"
    val = (name, mailID, passwords)
    cursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'User registered successfully.'})

@app.route('/login', methods=['POST'])
def login():
    name = request.json.get('name')
    passwords = request.json.get('passwords')
    cursor = mydb.cursor()
    cursor.execute("SELECT id, name, passwords FROM userDetails WHERE name=%s", (name,))
    user = cursor.fetchone()
    if user and passwords == user[2]:
        access_token = create_access_token(identity=user[0])
        print(access_token)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Invalid username or password"}), 401
    

if __name__ == '__main__':
    app.run()


