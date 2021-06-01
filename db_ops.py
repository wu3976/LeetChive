from pymysql.connections import Cursor
from config import dbname, dbhost, dbuser, dbpwd


def db_prep(cur: Cursor) -> None:
    cur.execute("create database if not exists {};".format(dbname))
    cur.execute("use {};".format(dbname))
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
        "create table if not exists startercodes({id}, {pID}, {starterCode}, {hint}, {primaryKey}, {foreign});".format(
            id="id int not null auto_increment",
            pID="pID int not null",
            starterCode="starterCode varchar(2500)",
            hint="hint varchar(2500)",
            primaryKey="primary key (id)",
            foreign="foreign key (pID) references problems(pID)"
        )
    )
    print(cur.fetchall())


# add a problem to the database
def db_add_problem(cur: Cursor, problemName: str, displayedName: str,
                   promptHtml: str, starterCode: str="", hint: str="") -> None:
    cur.execute(
        "insert into problems(problemName, displayedName, promptHtml)"
        + " values(\"{problemName}\", \"{displayedName}\", \"{promptHtml}\");".format(
            problemName=problemName,
            displayedName=displayedName,
            promptHtml=promptHtml
        )
    )
    print(cur.fetchall())
    cur.execute("select pID from problems order by pID desc;")
    pID = cur.fetchall()[0][0]
    cur.execute(
        "insert into startercodes(pID, starterCode, hint)"
        + " values({pID}, \"{starterCode}\", \"{hint}\");".format(
            pID=pID,
            starterCode=starterCode,
            hint=hint
        )
    )
    print(cur.fetchall())


def db_fetch_problems(cur: Cursor) -> list:
    cur.execute("select pID, displayedName from problems;")
    problems = cur.fetchall()
    result = []
    for pID, displayedName in problems:
        result.append({
            "pID": pID,
            "displayedName": displayedName,
        })
    return result


def db_fetch_problem(cur: Cursor, pID: int) -> dict:
    cur.execute("select * from problems where pID={};".format(pID))
    rawdata = cur.fetchall()
    result = {
        "pID": rawdata[0][0],
        "problemName": rawdata[0][1],
        "displayedName": rawdata[0][2],
        "promptHtml": rawdata[0][3]
    }
    return result


def db_fetch(cur: Cursor, ele: str, db:str, pID: int) -> str:
    cur.execute("select {ele} from {db} where pID={pID}".format(
        ele=ele,
        db=db,
        pID=str(pID)
    ))
    return cur.fetchall()[0][0]
