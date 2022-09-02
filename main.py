import mysql.connector
import os


def main():
    try:
        print(os.environ["MYSQL_ROOT_PASSWORD"])
    except KeyError as e:
        print("Environment variables not found")
        print(e)
    if not {"Database": dbName} in executeSQL("SHOW DATABASES", use=False):
        createDB()


def createDB():
    executeSQL("CREATE DATABASE " + dbName, use=False)
    executeSQL("""
    CREATE TABLE IF NOT EXISTS customers (
    id VARCHAR(15) PRIMARY KEY,
    coolData VARCHAR(30) NOT NULL) engine=InnoDB;
    """)


def executeSQL(command, parameters=(), use=True):
    try:
        database = mysql.connector.connect(**config)
        database.get_warnings = True
        cursor = database.cursor(dictionary=True)
    except mysql.connector.errors.ProgrammingError as e:
        print(e)
        exit()
    except mysql.connector.errors.DatabaseError as e:
        print("FATAL - MySQL probably doesn't exist on this system - {0}".format(e))
        exit()
    try:
        if use:
            cursor.execute("USE {0}".format(dbName))
        cursor.execute(command, parameters)
    except mysql.connector.errors.ProgrammingError as e:
        print("FATAL - Try dropping the whole database and retrying - {0}".format(e))
        exit()
    rows = cursor.fetchall()
    database.commit()
    database.close()
    return rows


if __name__ == '__main__':
    config = {
        "host": "localhost",
        "user": "root",
        "password": "cumcumcum"
    }
    dbName = "testDB"
    main()
