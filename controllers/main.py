from models.user import User
from models.message import Message
from controllers import clcrypto
from controllers.sql_connect import create_connection
import datetime

if __name__ == '__main__':
    # u_1 = User()
    # u_1.username = 'Antonii Kinper'
    # u_1.email = 'mail@mail.com'
    # u_1.set_password('abrakadabra', clcrypto.generate_salt())
    #
    # u_2 = User()
    # u_2.username = 'Klara Kinper'
    # u_2.email = 'mail2@mail.com'
    # u_2.set_password('hokuspokus', clcrypto.generate_salt())

    # u_3 = User()
    # u_3.username = 'Xaxaxa hahaha'
    # u_3.email = 'mail3@mail.com'
    # u_3.set_password('marokookoko', clcrypto.generate_salt())

    cnx = create_connection('warsztaty_2')
    cursor = cnx.cursor()

    # u_1.save_to_db(cursor)
    # u_2.save_to_db(cursor)
    # u_3.save_to_db(cursor)
    # a = User.load_user_by_id(cursor, 1)
    # print(a.username)
    # print(a.hashed_password)
    #
    # a = User.load_all_users(cursor)
    # for i in a:
    #     print(i.username)
    #     print(i.hashed_password)
    # m_1 = Message()
    # m_1.from_id = 3
    # m_1.to_id = 1
    # m_1.text = 'u la la la I'
    # m_1.creation_date = datetime.datetime.now()
    # m_2 = Message()
    # m_2.from_id = 3
    # m_2.to_id = 2
    # m_2.text = 'prezes naszego klubu'
    # m_2.creation_date = datetime.date.today().strftime('%Y-%m-%d')
    # m_1.save_to_db(cursor)
    a = Message.load_all_messages(cursor)
    for i in a:
        print(i.text)
