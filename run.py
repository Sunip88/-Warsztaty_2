import argparse
from controllers.sql_connect import create_connection
from controllers.clcrypto import check_password
from models.user import User
from psycopg2 import IntegrityError
import re


def check_email(email):
    pattern = re.compile(r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$')
    match = pattern.fullmatch(email)
    if match is not None:
        return False
    return True


def new_password(password):
    pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    match = pattern.match(password)
    while not match:
        print("Hasło powinno skladac sie z 8 znakow w tym jedna litera, jedna liczba i jeden znak specjalny")
        password = input('Podaj hasło:\n')
        match = pattern.fullmatch(password)
    return match.string


def new_name(name):
    while len(name) < 3:
        print("Nazwa użytkownika powinna ksłądać się z przynajmniej 3 znaków")
        name = input('Podaj Nazwe uzytkownika:\n')
    return name


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-n", "--new-pass", dest='newpass', help="User new password")
    parser.add_argument("-d", "--delete", dest='delete', default=False, action='store_true', help="Delete user")
    parser.add_argument("-e", "--edit", dest='edit', help="Change user password")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--list", dest='list', default=False, action='store_true', help="List all users")
    group.add_argument("-u", "--email", dest='email', help="User email")

    options, unknown = parser.parse_known_args()
    return options


def solution(options):
    cnx = None
    try:
        cnx = create_connection('warsztaty_2')
        user_obj = User()
        email = None
        password = None

        if options.email and options.password and not options.edit and not options.delete and not options.newpass:
            cursor = cnx.cursor()
            if user_obj.load_user_by_mail(cursor, options.email) is not None:
                email = user_obj.load_user_by_mail(cursor, options.email).email
                password = user_obj.load_user_by_mail(cursor, options.email).hashed_password
            if email is not None:
                if check_password(options.password, password):
                    print(f"Użytkownik o emailu {email} już istnieje")
                else:
                    print("Podane hasło jest błędne")
            else:
                try:
                    name = input('Podaj Nazwe uzytkownika:\n')
                    user_obj.username = new_name(name)
                    email_new = options.email
                    while check_email(email_new):
                        print("Adres email jest błędny. Proszę podaj adres w poprawnym formacie")
                        email_new = input('Podaj mail:\n')
                    user_obj.email = email_new
                    password_new = new_password(options.password)
                    user_obj.set_password(password_new, salt=None)
                    user_obj.save_to_db(cursor)
                    print(f"Użytkownik {user_obj.username} i email {user_obj.email} został utworzony")
                except IntegrityError as e:
                    print(e, "Proszę podać inny email")
            cursor.close()

        elif options.email and options.password and options.edit and not options.newpass \
                and not options.delete:
            cursor = cnx.cursor()
            user = user_obj.load_user_by_mail(cursor, options.email)
            if user is not None:
                password = user_obj.load_user_by_mail(cursor, options.email).hashed_password
                if check_password(options.password, password):
                    username_new = new_name(options.edit)
                    user.username = username_new
                    user.save_to_db(cursor)
                    print(f"Nazwa użytkownika o emailu {user.email} została zmieniona na {user.username}")
                else:
                    print("Hasło niepoprawne")
            else:
                print("Nie ma takiego użytkownika")
            cursor.close()

        elif options.email and options.password and options.newpass and not options.edit \
                and not options.delete:
            cursor = cnx.cursor()
            user = user_obj.load_user_by_mail(cursor, options.email)
            if user is not None:
                password = user_obj.load_user_by_mail(cursor, options.email).hashed_password
                if check_password(options.password, password):
                    password_new = new_password(options.newpass)
                    user.set_password(password_new, salt=None)
                    user.save_to_db(cursor)
                    print(f"Haslo dla uzytkownika {user.username} o emailu {user.email} zostało zmienione")
                else:
                    print("Hasło niepoprawne")
            else:
                print("Nie ma takiego użytkownika")
            cursor.close()

        elif options.email and options.password and options.delete and not options.edit \
                and not options.newpass:
            cursor = cnx.cursor()
            user = user_obj.load_user_by_mail(cursor, options.email)
            if user is not None:
                password = user_obj.load_user_by_mail(cursor, options.email).hashed_password
                if check_password(options.password, password):
                    answer = input("Czy jesteś pewien że chcesz usunąć użytkownika? (T/N)")
                    possibilities = ['T', 'N']
                    while answer not in possibilities:
                        answer = input("Czy jesteś pewien że chcesz usunąć użytkownika? (T/N)")
                    if answer == "T":
                        user.delete(cursor)
                        print(f"Uzytkownik o nazwie {user.username} i emailu {user.email} zostal usuniety")
                    else:
                        print("Przerwanie żądania")
                else:
                    print("Hasło niepoprawne")
            else:
                print("Nie ma takiego użytkownika")
            cursor.close()

        elif options.list and not options.edit and not options.delete and not options.newpass and not options.password:
            cursor = cnx.cursor()
            users_all = User().load_all_users(cursor)
            for user in users_all:
                for key, value in user.__dict__.items():
                    if key != '_User__hashed_password':
                        key = 'User Id' if key == '_User__id' else key
                        print('{}: {}'.format(key, value), end='\n')
                print('\n')
            cursor.close()

        else:
            print('Podaj parametr -h lub --help by zobaczyć możliwe parametry')
    except IntegrityError as e:
        print(e)
    finally:
        if cnx is not None:
            cnx.close()


if __name__ == '__main__':
    solution(set_options())
