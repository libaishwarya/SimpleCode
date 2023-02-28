from flask import Flask, jsonify,request
import mysql.connector as mysql

connection = mysql.connect(
  host="localhost",
  user="root",
  password="password",
  database="todoPro"
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

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
        return 'success'
    
@app.route("/showList", methods=['GET'])
def showData():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM userDetails")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM userDetails WHERE name = %s AND password = %s', (name, password))
        user = cursor.fetchone()
    return ({'status':'OK'})
    # return jsonify(user)
    # return 'logged in successfully'
    # return jsonify(user), 200

@app.route('/logout')
def logout():
    return ('logged out')
     
if __name__ == '__main__':
    app.run()
