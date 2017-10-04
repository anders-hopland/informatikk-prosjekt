window.onload = function () {
    let timeElem = document.getElementById("spnTime");
    if (timeElem) {
        document.getElementById("spnTime").innerHTML = new Date().toLocaleDateString();
    }
};