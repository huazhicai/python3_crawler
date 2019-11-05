import pyodbc

connect = pyodbc.connect('DRIVER= DRIVER=iSeries Access ODBC Driver;SYSTEM=10.0.0.1;SERVER=10.0.30.3,1433;DATABASE=master;UID=sa;PWD=Huamai521')

cursor = connect.cursor()

cursor.execute("select * from bbb")

rows = cursor.fetchall()
for row in rows:
    print(row)
