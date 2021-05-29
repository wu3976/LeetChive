/*var m0 = new Vue({
    id: "#m0",
    delimiters: ["[[", "]]"],
    methods: {
        redirectToIndex(event) {
            console.log("click");
            window.location.replace('/');
        }
    }
});*/

var d1 = new Vue({
    el: "#d1",
    delimiters: ["[[", "]]"],
    data: {
        submitButtonClass: "__buttonUp",
        hintButtonClass: "__buttonUp",
        testCases: [],
        msg: "",
        hint: ""
    },
    methods: {
        clickSubmit(event) {
            console.log("submit"); // TODO: handle click submit event
        },
        clickHint(event) {
            console.log("hint"); // TODO: handle click hint event
        },
        genRow(testCase) {
            return `xxx`; // TODO: write this function
        }
    }
    // TODO: add created property which fetch msg (initial code) from DB.
});