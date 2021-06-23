import pymysql, json, time, os
from flask import Flask, render_template, url_for, request
from db_ops import db_prep, db_add_problem, db_fetch_problems, \
    db_fetch_problem, db_fetch, db_setCol
from config import host, port, dbhost, dbuser, dbpwd, submit_dirname

app = Flask(__name__)

db = pymysql.connect(host=dbhost, user=dbuser, password=dbpwd, autocommit=True)
cur = db.cursor()
db_prep(cur)

submit_path = os.path.join(os.getcwd(), submit_dirname)

'''db_add_problem(
    cur=cur,
    problemName="test-problem",
    displayedName="Test Problem",
    promptHtml='this is the <span style=\\\"color:red\\\">test problem</span>',
    starterCode="int main(){}"
)'''


@app.route('/')
def index():
    context = {
        "scriptPath": url_for('static', filename='indexscript.js')
    }
    return render_template('index.html', context=context)


@app.route('/problems/<int:pID>')
def renderProblem(pID: int):
    problem = db_fetch_problem(cur, pID)
    return render_template('problem.html', context={
        "pID": problem["pID"],
        "problemName": problem["problemName"],
        "displayedName": problem["displayedName"],
        "promptHtml": problem["promptHtml"],
        "scriptPath": url_for('static', filename='problemscript.js')
    })


@app.route('/api/getProblemList')
def get_problem_list():
    return json.dumps(db_fetch_problems(cur))


@app.route('/api/getStarterCode/<int:pID>')
def get_starter_code(pID: int):
    return db_fetch(cur, "starterCode", "problems", pID)


@app.route('/api/getHint/<int:pID>')
def get_hint(pID: int):
    return db_fetch(cur, "hint", "problems", pID)


# json format: {
#   "problemName": str,
#   "displayedName": str,
#   "promptHtml": str,
#   "starterCode": str (optional),
#   "hint": str (optional),
#   "testCases": str (optional)
# }
# starter code format: better to a function that names the same with problemName.
# This function would be called by executor.
# test case format: testCases are snippets of c++ code.
# test case should print following to console:
# the first line is number of test cases
# the remaining column: <case_name>|<0 or 1>
@app.route('/api/add_problem', methods=['POST'])
def add_problem():
    if request.args.get("pwd") != "753951": # this is temporary.
        return "password incorrect&nbsp;<a href=\"/\">Main page</a>"
    print(request.get_data().decode('utf-8'))
    prob = json.loads(request.get_data().decode('utf-8'))

    if "problemName" not in prob or "displayedName" not in prob \
            or "promptHtml" not in prob:
        return "could not process json&nbsp;<a href=\"/\">Main page</a>"

    if "starterCode" not in prob:
        prob["starterCode"] = ""
    if "hint" not in prob:
        prob["hint"] = "Hint not avaliable"
    if "testCases" not in prob:
        prob["testCases"] = ""

    db_add_problem(cur, prob["problemName"], prob["displayedName"],
                   prob["promptHtml"], prob["starterCode"], prob["hint"], prob["testCases"])
    return "OK.&nbsp;<a href=\"/\">Main page</a>"


# json format: {
#   "col1_name": val_1,
#   "col2_name": val_2,
#   ...
# }
# can only set columns specified in modifiable_cols @ config
@app.route('/api/set_cols/<problemName>', methods=['POST'])
def setCols(problemName: str):
    if request.args.get("pwd") != "753951": # this is temporary.
        return "password incorrect&nbsp;<a href=\"/\">Main page</a>"
    datas = json.loads(request.get_data().decode('utf-8'))
    db_setCol(cur, problemName, datas)
    return "OK.&nbsp;<a href=\"/\">Main page</a>"


@app.route('/api/submit/<int:pID>', methods=['POST'])
def submitSolution(pID: int):
    fpath = os.path.join(submit_path, "{}_{}.cpp".format(pID, time.time()))
    file = open(fpath, "w+")
    file.write(request.get_data().decode('utf-8'))
    file.close()
    resp = [
        {
            "case": "test case",
            "correct": "aabbaa",
            "user": "aabaa",
            "status": "failed"
        },
        {
            "case": "test case 2",
            "correct": "blyat",
            "user": "blyat",
            "status": "success"
        }
    ]
    return json.dumps(resp)


if __name__ == '__main__':
    app.run(host=host, port=port)
