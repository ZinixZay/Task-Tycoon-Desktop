import psycopg2
from config import *

sql = psycopg2.connect(
    database=DB_NAME,
    user=USER_NAME,
    password=DB_PASSWORD,
    host=SERVER_HOST,
    port=SERVER_PORT
)

cur = sql.cursor()


def check_login_correctness(login, psw) -> bool:

    """
    try to compare 'password' from 'login' with 'psw'
    if they are similar return true
    else return false (even if login does not exist in the database)
    :param login: username which person enters
    :param psw: password which person enters
    :return: input correctness
    """

    com = f"SELECT password FROM app_users WHERE login=('{login}')"
    cur.execute(com)
    true_psw = cur.fetchall()
    if true_psw:
        if psw == true_psw[0][0]:
            return True
        else:
            return False
    else:
        return False


def get_task_titles(creator: str) -> list:
    com = f"SELECT var_name FROM variants WHERE creator=('{creator}')"
    cur.execute(com)
    titles = [title[0] for title in cur.fetchall()]
    return titles


def get_app_user_name(username: str) -> str:

    """
    finds a person with the somolar username and gets his name
    :param username: username of a person in the database
    :return: name of a person in the database
    """

    com = f"SELECT name FROM app_users WHERE login=('{username}')"
    cur.execute(com)
    return cur.fetchone()[0]
