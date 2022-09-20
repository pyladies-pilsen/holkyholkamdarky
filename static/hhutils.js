/* own functions */
"use strict";

deleteProtection(e) {
    if(document.getElementById('delete_confirmation').value !== "smazat")
    {
      alert("Pokud chcete vybraná přání skutečně smazat, napište do textového pole slovo 'smazat'");
      e.preventDefault()
    }
    // else, if formValid is true, the default behaviour will be executed.
}