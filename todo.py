from flask import Flask, jsonify,request,make_response
import mysql.connector as mysql
import jwt

connection = mysql.connect(
  host="localhost",
  user="root",
  password="password",
  database="todoPro"
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

data = {
    "muruga": "this is my todo list muruga",
    "AMP": "this is test thing"
}

@app.route('/registerPage', methods=['POST'])
def registerPage():
    if request.method == 'POST':
        name = request.form['name']
        emailId = request.form['emailId']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO userDetails(name, emailId,password) VALUES (%s, %s, %s)", (name, emailId, password))
        connection.commit()
        cursor.close()
        return '',200
    
@app.route("/showList", methods=['GET'])
def showData():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM userDetails")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userDetails WHERE name = %s AND password = %s', (name, password))
    user = cursor.fetchone()
    r = make_response(jsonify({
            "name": user[1],
            "emailId": user[2]
        }))
    r.headers["Authorization"] = jwt.encode({
            "name": user[1],
            "emailId": user[2],
            "userID": user[0]
        }, "mysecretkey", algorithm="HS256")
    return r, 200

@app.route('/getData')
def getData():
    authHeader = request.headers.get('Authorization')
    if authHeader:
        try:
            decodedData = jwt.decode(authHeader, key="mysecretkey", algorithms="HS256")
            userID = decodedData["userID"]
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM todoList WHERE userID  = %s', (userID,))
            todos = cursor.fetchall()
            result = []
            for i in todos:
                t = {
                    "id": i[0],
                    "todo": i[2]
                }
                result.append(t)
            return result, 200
        except Exception as e:
            print(e)
            return "", 401
    else:
        return "", 401
    
@app.route('/addTodo',methods=['POST'])
def addTodo():
    authHeader = request.headers.get('Authorization')
    if authHeader:
        try:
            decodedData = jwt.decode(authHeader, key="mysecretkey", algorithms="HS256")
            # TODO(aishu): add data here
            userID = decodedData["userID"]
            todo = request.form['todo']
            cursor = connection.cursor()
            cursor.execute("INSERT INTO todoList(userID, todo) VALUES (%s,%s)", (userID, todo))
            connection.commit()
            cursor.close()
            return "", 200
        except:
            return "", 401
    else:
        return "", 401
     
if __name__ == '__main__':
    app.run()
