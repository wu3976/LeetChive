// this will read from mysql in the future
var PROBLEMS = ["two-sum", "knapsack", "knight-move"]

var d1 = new Vue({
    el: "#d1",
    delimiters: ["[[", "]]"],
    data: {
        problems: PROBLEMS
    },
    methods: {
        getLink(p) {
            return `<a href='/problems/${p}'>${p}</a>`
        }
    }
});