// this will read from mysql in the future
var PROBLEMS = ["two-sum", "knapsack", "knight-move"]

var d1 = new Vue({
    el: "#d1",
    delimiters: ["[[", "]]"],
    data: {
        problems: [],
        pID: []
    },
    methods: {
        getLink(p, i) {
            return `<a href='/problems/${this.pID[i].toString()}'>${p}</a>`
        }
    },
    created() {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/api/getProblemList");
        xhttp.onreadystatechange = () => {
            if (xhttp.readyState === 4 && xhttp.status === 200){
                let problemsRaw = JSON.parse(xhttp.responseText);
                for (let i = 0; i < problemsRaw.length; i++){
                    this.problems.push(problemsRaw[i]["displayedName"]);
                    this.pID.push(problemsRaw[i]["pID"]);
                }
            }
        }
        xhttp.send();
    }
});