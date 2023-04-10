import pyodbc
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)

# Define the database connection details
server = 'your_server_name.database.windows.net'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
driver = '{ODBC Driver 17 for SQL Server}'

# Define the SQL query
query = "SELECT * FROM your_table_name WHERE volume > 990"

# Define the rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Define the API endpoint
class Data(Resource):
    decorators = [limiter.limit("10 per minute")]
    def get(self):
        try:
            # Establish a database connection
            conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")
            
            # Execute the SQL query
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Fetch the results
            data = cursor.fetchall()
            
            # Convert the results to a JSON format and return it as an API response
            response = jsonify(data)
            
            return response
        
        except Exception as e:
            # Handle any errors and return an error response
            error_message = f"An error occurred: {str(e)}"
            response = jsonify({"error": error_message})
            response.status_code = 500
            return response

api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(debug=True)
