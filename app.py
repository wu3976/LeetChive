import pymysql
from flask import Flask, render_template, url_for
from db_ops import db_prep, db_add_problem
from config import host, port, dbhost, dbuser, dbpwd

app = Flask(__name__)

db = pymysql.connect(host=dbhost, user=dbuser, password=dbpwd)
cur = db.cursor()
db_prep(cur)
db_add_problem(
    cur=cur,
    problemName="test-problem",
    displayedName="Test Problem",
    promptHtml='this is the <span style=\\\"color:red\\\">test problem</span>',
    starterCode="int main(){}"
)


@app.route('/')
def index():
    context = {
        "scriptPath": url_for('static', filename='indexscript.js')
    }
    return render_template('index.html', context=context)


@app.route('/problems/<name>')
def renderProblem(name: str):
    # in the future this would be fetched from database
    if name == "knight-move":
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
        return render_template('problem.html', context=context)


if __name__ == '__main__':
    app.run(host=host, port=port)
