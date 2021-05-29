from pymysql.connections import Cursor
from config import DBNAME, dbhost, dbuser, dbpwd


def db_prep(cur: Cursor) -> None:
    cur.execute("create database if not exists {};".format(DBNAME))
    cur.execute("use {};".format(DBNAME))
    print(cur.fetchall())
    cur.execute(
        "create table if not exists problems({pID}, {problemName}, {displayedName}, {promptHtml}, {primaryKey});".format(
            pID="pID int not null auto_increment",
            problemName="problemName varchar(50) not null",
            displayedName="displayedName varchar(50) not null",
            promptHtml="promptHtml varchar(2500) not null",
            primaryKey="primary key (pID)"
        )
    )
    print(cur.fetchall())
    cur.execute(
        "create table if not exists startercodes({pID}, {starterCode}, {primaryKey}, {foreign});".format(
            pID="pID int not null auto_increment",
            starterCode="starterCode varchar(2500)",
            primaryKey="primary key (pID)",
            foreign="foreign key (pID) references problems(pID)"
        )
    )
    print(cur.fetchall())


# add a problem to the database
def db_add_problem(cur: Cursor, problemName: str,
                   displayedName: str, promptHtml: str="", starterCode: str="") -> None:
    cur.execute(
        "insert into problems(problemName, displayedName, promptHtml)"
        + " values(\"{problemName}\", \"{displayedName}\", \"{promptHtml}\");".format(
            problemName=problemName,
            displayedName=displayedName,
            promptHtml = promptHtml
        )
    )
    print(cur.fetchall())
    cur.execute(
        "insert into startercodes(starterCode)"
        + " values(\"{starterCode}\");".format(
            starterCode=starterCode
        )
    )
    print(cur.fetchall())
