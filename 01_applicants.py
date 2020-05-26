import pyodbc
import mysql.connector

mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="rapidtest_dev"
)

mycursor = mysqldb.cursor()

server = 'tcp:localhost'
database = 'rapidtest'
username = 'relawan'
password = 'Covid192020!'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';PORT=1433')
mscursor = cnxn.cursor()

mscursor.execute("SELECT Id, FullName, Address, Email, PhoneNumber FROM AspNetUsers;")


def find_existing_row(code):
    sql = ("SELECT * FROM rdt_applicants WHERE registration_code = %s")
    val = (code,)
    mycursor.execute(sql, val)

    return mycursor.fetchone()


for row in mscursor.fetchall():
    print(row)

    exist = find_existing_row(row[0])

    if exist is None and len(row[0]) == 9:
        sql = "INSERT INTO rdt_applicants (registration_code, name, address, email, phone_number, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (row[0], row[1][0:100] if row[1] else None, row[2][0:190] if row[2] else None, row[3], row[4], 'NEW', '2020-05-26 12:00:00', '2020-05-26 12:00:00')
        mycursor.execute(sql, val)
        mysqldb.commit()
