from psycopg import connect

try:

    conn = connect(
        host="localhost",
        port=5432,
        dbname="ragdb",
        user="postgres",
        password="postgres"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    print("Connection successful!")
    print(version)

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)