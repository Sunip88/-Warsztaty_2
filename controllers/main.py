from models.users import User
from controllers import clcrypto
from controllers.sql_connect import create_connection


if __name__ == '__main__':
    u_1 = User()
    u_1.username = 'Antonii Kinper'
    u_1.email = 'mail@mail.com'
    u_1.set_password('abrakadabra', clcrypto.generate_salt())

    cnx = create_connection('warsztaty_2')
    cursor = cnx.cursor()

    u_1.save_to_db(cursor)