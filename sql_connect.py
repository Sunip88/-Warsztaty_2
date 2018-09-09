from psycopg2 import connect, OperationalError

def create_connection(db_name):
    username = "postgres"
    passwd = "coderslab"
    hostname = "localhost"  # lub "127.0.0.1"
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        cnx.autocommit = True
        print("Połączenie udane")
    except OperationalError as error:
        print(error)
        print("Brak połączenia")
    return cnx

def execute_sql(cnx, sql_file):
    cursor = cnx.cursor()
    file = open(sql_file, 'r')
    sql_text = file.read()
    file.close()

    sqlCommand = sql_text.split(";")
    print(sqlCommand)

    for command in sqlCommand:
        try:
            cursor.execute(command)
            print("Baza utworzona")
        except Exception as error:
            print("Nie udało się utorzyć tabeli, błąd", error)
    cursor.close()

if __name__ == "__main__":
    connection = create_connection("postgres")
    # execute_sql(connection, "a3_sql.sql")
    connection.close()