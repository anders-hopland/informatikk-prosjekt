let dropBtn = document.getElementById("dropBtn");
let dropDownMenu = document.getElementById("dropDownMenu");
console.log("hei");

dropBtn.onclick = function() {
    dropDownMenu.classList.toggle("show");
};

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    let dropdowns = document.getElementsByClassName("dropdown-content");

    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
};