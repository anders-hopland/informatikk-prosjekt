

// Kan henter fra databasen hvor mange titler eller verdier som trengs
// Setter disse inn i verdi 1, verdi2 osv.

let headValues = ["verdi1, verdi2, verdi3, verdi4, verdi5"];
let rader = ["rad1", "rad2", "rad3"];

// Henter ut elementene jeg skal håndtere i dashboard.html
let tabellen = document.getElementById("tabellen");
let tblTr = document.getElementById("tblTr");
let tblBody = document.getElementById("tblBody");

function createTable(headValues) {

    // Lager titlene i tabellen
    let newTr = document.createElement("tr");

    for (let i = 0; i < headValues.length; i++) {
        let newTh = document.createElement("th");
        newTh.innerHTML = headValues[i];
        newTr.appendChild(newTh);
    }

    tblTr.appendChild(newTr);
}

createTable(headValues);