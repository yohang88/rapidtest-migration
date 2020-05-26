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

mscursor.execute("SELECT Id, FullName, Address, Email, PhoneNumber, CAST(Registered AS NVARCHAR(4000)), City_IdCity, District_IdDistrict, Village_IdVillage FROM AspNetUsers;")


def find_existing_row(code):
    sql = ("SELECT * FROM rdt_applicants WHERE registration_code = %s")
    val = (code,)
    mycursor.execute(sql, val)

    return mycursor.fetchone()

def find_area(id):
    sql = ("SELECT code_kemendagri FROM areas WHERE id = %s")
    val = (id,)
    mycursor.execute(sql, val)

    return mycursor.fetchone()

for row in mscursor.fetchall():
    print(row)

    exist = find_existing_row(row[0])

    oldCode = row[0]
    oldName = row[1][0:100].strip().upper() if row[1] else None
    oldAddress = row[2][0:190].strip() if row[2] else None
    oldEmail = row[3].strip().lower()
    oldPhoneNumber = row[4].strip()
    oldRegistered = row[5][0:19] if row[5] != '0001-01-01 00:00:00.0000000 +00:00' else '2020-05-26 12:00:00'

    oldCityId = row[6]
    newCityCode = None

    if oldCityId:
        newCityCode = find_area(row[6])[0]

    oldDistrictId = row[7]
    newDistrictCode = None

    if oldDistrictId:
        newDistrictCode = find_area(row[7])[0]

    oldVillageId = row[8]
    newVillageCode = None

    if oldVillageId:
        newVillageCode = find_area(row[8])[0]

    if exist is None:
        if len(row[0]) == 9:
            sql = "INSERT INTO rdt_applicants (registration_code, name, province_code, city_code, district_code, village_code, address, email, phone_number, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row[0], oldName, '32', newCityCode, newDistrictCode, newVillageCode, oldAddress, oldEmail, oldPhoneNumber, 'NEW', oldRegistered, '2020-05-26 12:00:00')
            mycursor.execute(sql, val)
            mysqldb.commit()
    else:
        sql = "UPDATE rdt_applicants SET name = %s, province_code = %s, city_code = %s, district_code = %s, village_code = %s, address = %s, email = %s, phone_number = %s, created_at = %s, updated_at = %s WHERE registration_code = %s"
        val = (oldName, '32', newCityCode, newDistrictCode, newVillageCode, oldAddress, oldEmail, oldPhoneNumber, oldRegistered, '2020-05-26 12:00:00', oldCode)
        mycursor.execute(sql, val)
        mysqldb.commit()
