from flask import Flask, request, jsonify
import mysql.connector
app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD",
    database="student"
)

@app.route('/user', methods=['POST'])
def add_user():
    user_data = request.json
    name = user_data['name']
    subject = user_data['subject']
    mark = user_data['mark']
    
    cursor = db.cursor()
    # Prepare the SQL query to insert user details
    query = "INSERT INTO students_detail (name, subject, mark) VALUES (%s, %s, %s)"
    values = (name, subject, mark)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    # Return a success message
    return jsonify({'message': 'User details added successfully'})

@app.route('/user/<int:id>', methods=['GET'])
def get_user_details(id):
    try:        
        cursor = db.cursor()
        # Retrieve user details based on the user ID
        query = "SELECT * FROM students_detail WHERE id = %s"
        cursor.execute(query, (id,))
        # db.commit()
        user = cursor.fetchone()
        db.commit()
        if user:
            # Format the user details into a JSON response
            user_details = {
                'id': user[0],
                'name': user[1],
                'subject': user[2],
                'mark': user[3],
            }
            return jsonify(user_details)
        else:
            return jsonify({'message': 'User not found'})
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})
    # Return a success message
    return jsonify({'message': 'User details added successfully'})

@app.route('/user/<int:id>', methods=['PUT'])
def edit_user(id):
    # Get the updated user details from the request
    updated_user = request.get_json()
   
    cursor = db.cursor()
    try:
        # Update the user details in the database
        update_query = "UPDATE students_detail SET name=%s, mark=%s WHERE id=%s"
        cursor.execute(update_query, (updated_user['name'], updated_user['mark'],id))
        db.commit()
        return jsonify({'message': 'User details updated successfully'})
    except mysql.connector.Error as err:
        # Handle any database errors
        print(f"Error updating user details: {err}")
        return jsonify({'error': 'Failed to update user details'}), 500
    
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
      
        # cursor = connection.cursor()
        cursor = db.cursor()
        # Execute the DELETE query
        delete_query = "DELETE FROM students_detail WHERE id = %s"
        cursor.execute(delete_query, (id,))
        db.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return f"User with ID {id} deleted successfully."
        else:
            return f"User with ID {id} not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"  
 
if __name__ == '__main__':
    app.run()