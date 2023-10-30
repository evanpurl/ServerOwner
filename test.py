from utils.sqlite import create_db, create_table, createuniqueindex, newticket, insertdate, get_datetime, get_alltickets
from sqlite3 import Error
from datetime import datetime


def ticket():
    try:
        db = create_db("storage/tickets.db")
        create_table(db, """CREATE TABLE IF NOT EXISTS tickets ( userid bigint, channel bigint, datetime text); """)
        createuniqueindex(db, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_userid ON tickets (userid) """)
        print(f"Database set up")
    except Error as e:
        print(e)


def createticket():
    try:
        db = create_db("storage/tickets.db")
        newticket(db, 123456789, 987654321)
        print("Ticket Added into database")
    except Error as e:
        print(e)


def insertdatetime():
    try:
        conn = create_db(f"storage/tickets.db")
        for a in get_alltickets(conn):
            time_till = datetime.strptime(a[2], '%Y-%m-%d %H:%M:%S.%f') - datetime.now()
            print(time_till.total_seconds())
    except Error as e:
        print(e)


insertdatetime()
