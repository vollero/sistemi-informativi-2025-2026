const filterInput = document.querySelector("#filterInput");
const schede = Array.from(document.querySelectorAll("#schedeList li"));
const counterButton = document.querySelector("#counterButton");
const counterValue = document.querySelector("#counterValue");

if (filterInput) {
  filterInput.addEventListener("input", () => {
    const query = filterInput.value.trim().toLowerCase();
    schede.forEach((scheda) => {
      const testo = scheda.dataset.search;
      scheda.hidden = query !== "" && !testo.includes(query);
    });
  });
}

if (counterButton && counterValue) {
  let count = 0;
  counterButton.addEventListener("click", () => {
    count += 1;
    counterValue.textContent = count;
  });
}
