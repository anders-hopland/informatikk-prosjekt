window.onload = function () {
    let timeElem = document.getElementById("spnTime");
    if (timeElem) {
        timeElem.innerHTML = new Date().toLocaleDateString();
    }
};