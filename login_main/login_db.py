from PySide6.QtSql import QSqlDatabase, QSqlQuery
from sqlalchemy import func

ACCOUNTS_SQL= """
                CREATE TABLE ACCOUNTS
                (SYS_ID INTEGER, 
                ID VARCHAR PRIMARY KEY, 
                PASSWORD INTEGER)
             """

SYSTEMS_SQL= """
                CREATE TABLE SYSTEMS(
                    SYS_ID INTEGER PRIMARY KEY, 
                    SYS_NAME VARCHAR
                )
             """

INSERT_ACCOUNT_SQL= """
                        INSERT INTO ACCOUNTS(SYS_ID, ID, PASSWORD)
                        SELECT S.SYS_ID, ?, ?
                        FROM SYSTEMS_SQL
                        WHERE S.SYS_ID= ?;
                    """

INSERT_SYSTEM_SQL= """INSERT INTO SYSTEMS(SYS_ID, SYS_NAME) VALUES (?, ?)"""

def add_account(q, id, password):
    q.addBindValue(id)
    q.addBindValue(password)
    q.exec()

def add_system(q, sys_id, sys_name):
    q.addBindValue(sys_id)
    q.addBindValue(sys_name)
    q.exec()

    return q.lastInsertId()

def init_db():
    def check(func, *args):
        if not func(*args): raise ValueError(func.__self__.lastError())

    db= QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    check(db.open)

    q= QSqlQuery()

    check(q.exec, ACCOUNTS_SQL)
    check(q.exec, SYSTEMS_SQL)

    add_system(q, 1, "security")
    add_system(q, 2, "intersection")
    add_system(q, 3, "schoolzone")
    add_system(q, 4, "left_turn")

    add_account(q, 0, "administrator", 1234)
    add_account(q, 1, "sec", 1234)
    add_account(q, 2, "its", 1234)
    add_account(q, 3, "sch", 1234)
    add_account(q, 4, "lft", 1234)

    return db