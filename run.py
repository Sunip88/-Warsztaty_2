import argparse
from controllers.sql_connect import create_connection
from controllers.clcrypto import check_password
from models.user import User
from psycopg2 import IntegrityError
import sys
import re


def check_email(email):
    pattern = re.compile(r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$')
    match = pattern.fullmatch(email)
    if match is not None:
        return False
    return True


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest='username', help="User login")
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-n", "--new-pass", dest='newpass', help="User new password")
    parser.add_argument("-l", "--list", dest='list', default=False, help="List all users")
    parser.add_argument("-d", "--delete", dest='delete', help="Delete user")
    parser.add_argument("-e", "--edit", dest='edit',  help="Change user login")
    try:
        options = parser.parse_args()
        return options
    except:
        parser.print_help()
        sys.exit(0)


def solution(options):
    cnx = create_connection('warsztaty_2')
    cursor = cnx.cursor()
    user_obj = User()
    email = None
    password = None

    if (options.username and options.password) and (not options.edit and not options.delete):
        if user_obj.load_user_by_name(cursor, options.username) is not None:
            email = user_obj.load_user_by_name(cursor, options.username).email
            password = user_obj.load_user_by_name(cursor, options.username).hashed_password
        if email is not None:
            if check_password(options.password, password):
                print(f"Użytkownik o email: {email} już istnieje")
            else:
                print("Podane hasło jest błędne")
        else:
            try:
                user_obj.username = options.username
                email_new = input('Podaj mail:\n')
                while check_email(email_new):
                    print("Adres email jest błędny. Proszę podaj adres w poprawnym formacie")
                    email_new = input('Podaj mail:\n')
                user_obj.email = email_new
                password_new = options.password
                while len(password_new) < 8:
                    print("Hasło jest za krótkie. Prosze podaj hasło które ma przynajmniej 8 znaków")
                    password_new = input('Podaj hasło:\n')
                user_obj.set_password(password_new, salt=None)
                user_obj.save_to_db(cursor)
                print(f"Użytkownik {user_obj.username} i email {user_obj.email} został utworzony")
            except IntegrityError as e:
                print(e, "Proszę podać inny email")

    elif options.username and options.password and options.edit:
        pass

    elif options.username and options.password and options.delete:
        pass
    elif options.list:
        pass

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    solution(set_options())
