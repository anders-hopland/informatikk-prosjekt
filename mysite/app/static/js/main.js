/**
 * Funksjonen sjekker om tabellbodyen er tom.
 * Deretter erstatter den tabellen med en p som sier
 * at ingenting er registrert
 */
window.onload = function() {
    let overview = document.getElementById("overview");
    let tableBody = document.getElementById("tableBdy");

    if (!tableBody) {
        return;
    }


    if (tableBody.children.length === 0) {
        let newP = document.createElement("p");
        newP.innerHTML = "Du har ikke noe registrert.";
        newP.className = "greyed";
        overview.innerHTML = "";
        overview.appendChild(newP);
    }
};

