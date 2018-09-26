import argparse
from controllers.sql_connect import create_connection
from controllers.clcrypto import check_password
from models.user import User
from models.message import Message
from psycopg2 import IntegrityError
import datetime
import re


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest='username', help="User name")
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-l", "--list", dest='list', default=False, action='store_true', help="List all messages")
    parser.add_argument("-t", "--to", dest='to', help="Email adress of recipient")
    parser.add_argument("-s", "--send", dest='send', default=False, help="sent message")

    options, unknown = parser.parse_known_args()
    return options

def solution(options):
    cursor = None
    cnx = None
    try:
        cnx = create_connection('warsztaty_2')
        cursor = cnx.cursor()
        user = None
        user_to = None
        password = None

        if options.username and options.password and options.list and not options.to and not options.send:
            user = User.load_user_by_name(cursor, options.username)
            if user is not None:
                password = user.hashed_password
                if check_password(options.password, password):
                    messages = Message.load_all_message_for_user(cursor, user.id)
                    for message in messages:
                        for key, value in message.__dict__.items():
                            if key != '_Message__hashed_password':
                                key = 'Message Id' if key == '_Message__id' else key
                                print('{}: {}'.format(key, value), end='\n')
                        print('\n')
                else:
                    print("Podane hasło jest błędne")
            else:
                print("Podany uzytkownik nie istnieje")

        elif options.username and options.password and options.to and options.send and not options.list:
            user = User.load_user_by_name(cursor, options.username)
            user_to = User.load_user_by_mail(cursor, options.to)
            if user is not None and user_to is not None:
                password = user.hashed_password
                if check_password(options.password, password):
                    if options.send != '':
                        msg = Message()
                        msg.from_id = user.id
                        msg.to_id = user_to.id
                        msg.text = options.send
                        msg.creation_date = datetime.datetime.now()
                        msg.save_to_db(cursor)
                        print(f"Wiadomosc zostala wyslana do {user_to.username} na email {user_to.email} o tresci '{msg.text}'")
                else:
                    print("Podane hasło jest błędne")
            else:
                if user is None:
                    print("Zly login, prosze podac wlasciwa nazwe uzytkownika")
                elif user_to is None:
                    print("Uzytkownik o podanym mailu nie istnieje")

        else:
            print('Brak funkcjonalnosci dla podanych parametrów')
    except IntegrityError as e:
        print(e)
    finally:
        if cnx is not None:
            cursor.close()
            cnx.close()


if __name__ == '__main__':
    solution(set_options())