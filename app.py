from flask import Flask, render_template, request, jsonify
import pyodbc
app = Flask(__name__)
# Replace these values with your Azure SQL Database information
server = 'training.caaklpetxrbl.ap-south-1.rds.amazonaws.com'
database = 'userdb'
username = 'apitool'
password = 'qsCs8aAL0498kDy5'
driver = '{ODBC Driver 17 for SQL Server}'
# Establish a connection to the Azure SQL Database
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Create a table if it doesn't exist
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'UserData')
    BEGIN
        CREATE TABLE UserData (
            id INT PRIMARY KEY IDENTITY(1,1),
            first_name NVARCHAR(50),
            last_name NVARCHAR(50)
        );
    END
''')
conn.commit()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/save', methods=['POST'])
def save():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    # Save data to the database
    cursor.execute("INSERT INTO UserData (first_name, last_name) VALUES (?, ?)", first_name, last_name)
    conn.commit()
    return "Data saved successfully!"
@app.route('/api', methods=['POST'])
def api():
    try:
        # Extract data from the JSON request
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        # Save data to the database
        cursor.execute("INSERT INTO UserData (first_name, last_name) VALUES (?, ?)", first_name, last_name)
        conn.commit()
        response = {'status': 'success', 'message': 'Data saved successfully!'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return jsonify(response)
# ... (remaining code)
@app.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve data from the database
    cursor.execute("SELECT * FROM UserData")
    data = cursor.fetchall()
    # Display the data
    result = ""
    for row in data:
        result += f"ID: {row.id}, First Name: {row.first_name}, Last Name: {row.last_name}<br>"
    return result
if __name__ == '__main__':
    app.run(debug=True)
