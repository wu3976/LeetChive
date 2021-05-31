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
        hint: "",
        pID: ""
    },
    methods: {
        clickSubmit(event) {
            console.log("submit"); // TODO: handle click submit event
        },
        clickHint(event) {
            let xhttp = new XMLHttpRequest();
            xhttp.open("GET", `/api/getHint/${this.pID}`);
            xhttp.onreadystatechange = () => {
                if (xhttp.readyState === 4 && xhttp.status === 200){
                    this.hint = xhttp.responseText;
                }
            };
            xhttp.send();
        },
        genRow(testCase) {
            return `xxx`; // TODO: write this function
        }
    },
    created() {
        this.pID = document.getElementById("pID").innerText;
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", `/api/getStarterCode/${this.pID}`);
        xhttp.onreadystatechange = () => {
            if (xhttp.readyState === 4 && xhttp.status === 200){
                this.msg = xhttp.responseText;
            }
        };
        xhttp.send();
    }
});