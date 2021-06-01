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
        // [{
        //  "case": xxx,
        //  "correct": xxx,
        //  "user": xxx,
        //  "success": True/False
        // },...]
        testCases: [],
        msg: "",
        hint: "",
        pID: ""
    },
    methods: {
        clickSubmit(event) {
            let xhttp = new XMLHttpRequest();
            xhttp.open("POST", `/api/submit/${this.pID}`);
            xhttp.onreadystatechange = () => {
                if (xhttp.readyState === 4 && xhttp.status === 200){
                    this.testCases = JSON.parse(xhttp.responseText);
                }
            };
            xhttp.send(this.msg);
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
            let html = ``, ks = Object.keys(testCase)
            for (let i = 0; i < ks.length; i++){
                html += `<td class="cell">${testCase[ks[i]]}</td>`
            }
            return html;
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