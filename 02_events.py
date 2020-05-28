import pyodbc
import mysql.connector
from datetime import datetime
import pytz
import random

mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="rapidtest_dev",
    charset="utf8mb4"
)

mycursor = mysqldb.cursor()

server = 'tcp:localhost'
database = 'rapidtest'
username = 'relawan'
password = 'Covid192020!'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';PORT=1433')
mscursor = cnxn.cursor()

mscursor.execute("SELECT Programs.IdProgram, Programs.Title, CAST(Programs.Start AS NVARCHAR(4000)), CAST(Programs.Finish AS NVARCHAR(4000)), Locations.Address FROM Programs JOIN Locations ON Programs.Location_IdLocation = Locations.IdLocation")


def get_event_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code

def update_participant_event_id(old_id_program, inserted_id):
    sql = ("SELECT Participant_Id FROM ProgramTransactions WHERE Program_IdProgram = ?")
    val = (old_id_program,)
    mscursor.execute(sql, val)

    for row in mscursor.fetchall():
        print(row)
        sql = "UPDATE rdt_applicants SET rdt_event_id = %s WHERE registration_code = %s"
        val = (inserted_id, row[0])
        mycursor.execute(sql, val)
        mysqldb.commit()

for row in mscursor.fetchall():
    print(row)

    old_id_program = row[0]
    old_event_name = row[1]
    old_event_start = row[2][0:19]
    old_event_end = row[3][0:19]
    old_address = row[4]

    start_datetime = datetime.strptime(old_event_start, "%Y-%m-%d %H:%M:%S")
    finish_datetime = datetime.strptime(old_event_end, "%Y-%m-%d %H:%M:%S")

    local = pytz.timezone("Asia/Jakarta")

    start_local_dt = local.localize(start_datetime, is_dst=None)
    start_utc_dt = start_local_dt.astimezone(pytz.utc)

    finish_local_dt = local.localize(finish_datetime, is_dst=None)
    finish_utc_dt = finish_local_dt.astimezone(pytz.utc)

    new_start_datetime = start_utc_dt.strftime("%Y-%m-%d %H:%M:%S")
    new_finish_datetime = finish_utc_dt.strftime("%Y-%m-%d %H:%M:%S")

    new_event_code = get_event_code(6)

    sql = "INSERT INTO rdt_events (event_code, event_name, event_location, start_at, end_at, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (new_event_code, old_event_name, old_address, new_start_datetime, new_finish_datetime, 'PUBLISHED', '2020-05-26 12:00:00', '2020-05-26 12:00:00')

    mycursor.execute(sql, val)
    mysqldb.commit()

    inserted_id = mycursor.lastrowid

    update_participant_event_id(old_id_program, inserted_id)

