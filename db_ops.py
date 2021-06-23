from pymysql.connections import Cursor
from config import dbname, dbhost, dbuser, dbpwd, modifiable_cols


def db_prep(cur: Cursor) -> None:
    cur.execute("create database if not exists {};".format(dbname))
    cur.execute("use {};".format(dbname))
    print(cur.fetchall())
    cur.execute(
        "create table if not exists problems({pID}, {problemName}, {displayedName}, {promptHtml}, \
        {starterCode}, {hint}, {testCases}, {primaryKey});".format(
            pID="pID int not null auto_increment",
            problemName="problemName varchar(50) unique not null",
            displayedName="displayedName varchar(50) not null",
            promptHtml="promptHtml text not null",
            starterCode="starterCode text not null",
            hint="hint text not null",
            testCases="testCases text not null",
            primaryKey="primary key (pID)"
        )
    )
    print(cur.fetchall())


# add a problem to the database
def db_add_problem(cur: Cursor, problemName: str, displayedName: str,
                   promptHtml: str, starterCode: str="",
                   hint: str="", testCases: str="") -> None:
    print("insert into problems(problemName, displayedName, promptHtml, starterCode, \
        hint, testCases)"
        + " values(\"{problemName}\", \"{displayedName}\", \"{promptHtml}\", \"{starterCode}\", \"{hint}\", \"{testCases}\");".format(
            problemName=problemName,
            displayedName=displayedName,
            promptHtml=promptHtml,
            starterCode=starterCode,
            hint=hint,
            testCases=testCases
        ))
    cur.execute(
        "insert into problems(problemName, displayedName, promptHtml, starterCode, \
        hint, testCases)"
        + " values(\"{problemName}\", \"{displayedName}\", \"{promptHtml}\", \"{starterCode}\", \"{hint}\", \"{testCases}\");".format(
            problemName=problemName,
            displayedName=displayedName,
            promptHtml=promptHtml,
            starterCode=starterCode,
            hint=hint,
            testCases=testCases
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


def db_setCol(cur: Cursor, at: str, datas: dict) -> None:
    for k in datas.keys():
        if k not in modifiable_cols:
            raise "Column " + str(k) + " is unmodifiable"
        print(datas)
    for k in datas.keys():
        cur.execute("update problems set {col}=\"{val}\" where problemName=\"{pname}\";".format(
            col=k, val=datas[k], pname=at
        ))
        cur.fetchall()