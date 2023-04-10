# import necessary modules
import pyodbc
from rest_framework.response import Response
from rest_framework.views import APIView

class AzureSQLTable(APIView):
    def get(self, request):
        # set up connection to Azure SQL DB
        server = 'your_server_name.database.windows.net'
        database = 'your_database_name'
        username = 'your_username'
        password = 'your_password'
        driver = '{ODBC Driver 17 for SQL Server}'
        cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = cnxn.cursor()

        # execute SQL query to get data from table
        cursor.execute('SELECT * FROM your_table_name')
        rows = cursor.fetchall()

        # format data as JSON response
        data = []
        for row in rows:
            data.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                # add more fields as needed
            })

        return Response(data)
