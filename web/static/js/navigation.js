const items = document.querySelectorAll(".item");
let currentIndex = 0;

function updateSelection() {
  items.forEach(i => i.classList.remove("selected"));
  items[currentIndex].classList.add("selected");
}


// initial highlight
updateSelection();

document.addEventListener("keydown", (e) => {

  if (e.key === "ArrowRight" || e.key === "ArrowDown") {
    currentIndex = (currentIndex + 1) % items.length;
    updateSelection();
  }

  if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    updateSelection();
  }

  if (e.key === "Enter") {
    const url = items[currentIndex].dataset.url;
    window.location.href = url; // load new page
  }
});

// mouse click also works
items.forEach(item => {
  item.addEventListener("click", () => {
    window.location.href = item.dataset.url;
  });
});

