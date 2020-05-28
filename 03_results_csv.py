import csv
import mysql.connector

mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="rapidtest_dev",
    charset="utf8mb4"
)

mycursor = mysqldb.cursor()

def find_applicant(code):
    sql = ("SELECT id FROM rdt_applicants WHERE registration_code = %s")
    val = (code,)
    mycursor.execute(sql, val)

    return mycursor.fetchone()

with open('csv/hasil_test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        registration_code = row[0]
        result = row[1]

        applicant = find_applicant(registration_code)

        if applicant:
            applicant_id = applicant[0]

            sql = "INSERT INTO rdt_lab_results (rdt_applicant_id, lab_result_type, created_at, updated_at) VALUES (%s, %s, %s, %s)"
            val = (applicant_id, result, '2020-05-26 12:00:00', '2020-05-26 12:00:00')
            mycursor.execute(sql, val)
            mysqldb.commit()
