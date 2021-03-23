from os.path import isfile
from sqlite3 import connect

DB_PATH = "./data/db/database.db"  # path of the database(constant)
BUILD_PATH = "./data/db/build.sql"  # path of command to build database

cxn = connect(DB_PATH, check_same_thread=False)  # connection to database, accesses data inside
cur = cxn.cursor()  # cursor object to retrieve data one row at a time from a result set


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit  # means build = with_commit(build)
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def commit():
    cxn.commit()  # saves data


def close():
    cxn.close()  # closes connection


def field(command, *values):
    cur.execute(command, tuple(values))  # runs an SQL command

    if fetch := cur.fetchone() is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()  # retrieves next result of a query result set and returns a tuple


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()  # retrieves all results of a query result set and returns a list of tuples


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    cur.executemany((command, valueset))  # runs an SQL command many times with different values


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
