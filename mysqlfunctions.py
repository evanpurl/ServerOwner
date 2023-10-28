import aiomysql

# Database connection parameters
DB_HOST = "172.18.0.1"
DB_PORT = 3306
DB_USER = "u42_KWztg3tCWJ"
DB_PASSWORD = "VbtJ@d+SLdRpZz0^!jJAQiom"
DB_NAME = "s42_serverowner"

async def create_db_connection():
    try:
        connection = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
        )
        return connection
    except aiomysql.MySQLError as err:
        print(f"Error connecting to the database: {err}")
        return None

async def get_config(connection, guild_id, key):
    try:
        async with connection.cursor() as cursor:
            query = "SELECT value FROM config WHERE guild_id = %s AND key = %s"
            await cursor.execute(query, (guild_id, key))
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    except aiomysql.MySQLError as err:
        print(f"Error fetching config from the database: {err}")
        return None
