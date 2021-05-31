import pymysql, json
from flask import Flask, render_template, url_for, request
from db_ops import db_prep, db_add_problem, db_fetch_problems, \
    db_fetch_problem, db_fetch
from config import host, port, dbhost, dbuser, dbpwd

app = Flask(__name__)

db = pymysql.connect(host=dbhost, user=dbuser, password=dbpwd, autocommit=True)
cur = db.cursor()
db_prep(cur)

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
    # in the future this would be fetched from database
    '''if name == "knight-move":
        context = {
            "pID": str(2),
            "problemName": "knight-move",
            "displayedName": "Knight Move",
            "promptHtml": 'Given an <span class="code">boardSize</span> x <span class="code">boardSize</span> chessBoard,'
                          + 'a horse is at the upper-left corner of the board. <br>'
                          + 'Find the number of ways this horse can reach to the lower-right'
                          + 'corner in <br><span class="code">moves</span> steps.',
            "scriptPath": url_for('static', filename='problemscript.js')
        }
        return render_template('problem.html', context=context)'''
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
    return db_fetch(cur, "starterCode", "startercodes", pID)


@app.route('/api/getHint/<int:pID>')
def get_hint(pID: int):
    return db_fetch(cur, "hint", "startercodes", pID)


# json format: {
#   "problemName": str,
#   "displayedName": str,
#   "promptHtml": str,
#   "starterCode": str (optional),
#   "hint": str (optional)
# }
@app.route('/api/add_problem', methods=['POST'])
def add_problem():
    if request.args.get("pwd") != "753951": # this is temporary.
        return "password incorrect&nbsp;<a href=\"/\">Main page</a>"
    prob = json.loads(request.get_data().decode('utf-8'))
    if "problemName" not in prob or "displayedName" not in prob \
            or "promptHtml" not in prob:
        return "could not process json&nbsp;<a href=\"/\">Main page</a>"
    if "starterCode" not in prob:
        prob["starterCode"] = ""
    if "hint" not in prob:
        prob["hint"] = "Hint not avaliable"
    db_add_problem(cur, prob["problemName"], prob["displayedName"],
                   prob["promptHtml"], prob["starterCode"], prob["hint"])
    return "OK.&nbsp;<a href=\"/\">Main page</a>"


if __name__ == '__main__':
    app.run(host=host, port=port)
