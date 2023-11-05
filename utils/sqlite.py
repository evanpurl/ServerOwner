import sqlite3
from sqlite3 import Error


async def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error or Exception as e:
        print(f"create db: {e}")


async def create_table(conn, tabledata):
    """ create a table from the create_table_sql statement
    :param tabledata: Data to create in table
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(tabledata)
        c.close()

    except Error or Exception as e:
        print(f"create table: {e}")


async def newticket(conn, user, channel):
    try:
        datatoinsert = f""" REPLACE INTO tickets(userid, channel) VALUES( ?, ?) """
        c = conn.cursor()
        c.execute(datatoinsert, (user.id, channel))  # Replace with user.id
        conn.commit()
        c.close()
        print(f"New Ticket created by user {user.name}")  # replace with user.name

    except Error or Exception as e:
        print(f"New Ticket: {e}")


async def insertdate(conn, channel, datetime):
    try:
        datatoinsert = f""" UPDATE tickets SET datetime=? WHERE channel=? """
        c = conn.cursor()
        c.execute(datatoinsert, (datetime, channel))
        conn.commit()
        c.close()
    except Error or Exception as e:
        print(f"Insert Date: {e}")


async def createuniqueindex(conn, datatoinsert):
    try:
        c = conn.cursor()
        c.execute(datatoinsert)
        conn.commit()
        c.close()
    except Error or Exception as e:
        print(f"createuniqueindex: {e}")


async def get_datetime(conn, user):
    c = conn.cursor()
    c.execute(""" SELECT date(datetime), time(datetime) FROM tickets WHERE userid=? """, [user])
    option = c.fetchone()
    return option


async def get_user(conn, channel):
    c = conn.cursor()
    c.execute(""" SELECT userid FROM tickets WHERE channel=? """, [channel])
    option = c.fetchone()
    if option:
        return option[0]
    else:
        return None


async def if_user_ticket(conn, user):
    c = conn.cursor()
    c.execute(""" SELECT userid, channel FROM tickets WHERE userid=? """, [user.id])
    option = c.fetchall()
    return option


async def get_alltickets(conn):
    c = conn.cursor()
    c.execute(""" SELECT * FROM tickets""")
    option = c.fetchall()
    return option


async def removedate(conn, channel):
    try:
        datatoinsert = f""" UPDATE tickets SET datetime=? WHERE channel=? """
        c = conn.cursor()
        c.execute(datatoinsert, (None, channel))
        conn.commit()
        c.close()
    except Error or Exception as e:
        print(f"Remove Date: {e}")


async def remove(conn, user):
    try:
        datatoinsert = f""" DELETE from tickets WHERE userid=? """
        c = conn.cursor()
        c.execute(datatoinsert, (user.id,))
        conn.commit()
        c.close()
    except Error or Exception as e:
        print(f"Remove ticket: {e}")


async def ticket():
    try:
        db = await create_db("storage/tickets.db")
        await create_table(db,
                           """CREATE TABLE IF NOT EXISTS tickets ( userid bigint, channel bigint, datetime text); """)
        await createuniqueindex(db, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_userid ON tickets (userid) """)
        print(f"Ticket database has been set up.")
    except Error as e:
        print(e)


async def get_warnings(conn, userid):
    try:
        c = conn.cursor()
        c.execute(""" SELECT reason FROM warnings WHERE userid=? """, [userid])
        option = c.fetchall()
        c.close()
        conn.close()
        if option:
            return option
        else:
            return None

    except Exception or Error as e:
        print(f"get warnings: {e}")


async def insert_warning(conn, configlist):
    # config list should be a length of 2.
    try:
        datatoinsert = f""" INSERT INTO warnings(userid, reason) VALUES( ?, ?) """
        c = conn.cursor()
        c.execute(datatoinsert, (configlist[0], str(configlist[1])))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"insert warning: {e}")


async def remove_warnings(conn, user):
    try:
        datatoinsert = f""" DELETE from warnings WHERE userid=? """
        c = conn.cursor()
        c.execute(datatoinsert, (user,))
        conn.commit()
        c.close()
    except Error or Exception as e:
        print(f"Remove warnings: {e}")
