from models.users import User
from controllers import clcrypto
from controllers.sql_connect import create_connection


if __name__ == '__main__':
    u_1 = User()
    u_1.username = 'Antonii Kinper'
    u_1.email = 'mail@mail.com'
    u_1.set_password('abrakadabra', clcrypto.generate_salt())

    u_2 = User()
    u_2.username = 'Klara Kinper'
    u_2.email = 'mail2@mail.com'
    u_2.set_password('hokuspokus', clcrypto.generate_salt())

    cnx = create_connection('warsztaty_2')
    cursor = cnx.cursor()

    # u_1.save_to_db(cursor)
    # u_2.save_to_db(cursor)
    a = User.load_user_by_id(cursor, 1)
    print(a.username)
    print(a.hashed_password)

    a = User.load_all_users(cursor)
    for i in a:
        print(i.username)
        print(i.hashed_password)