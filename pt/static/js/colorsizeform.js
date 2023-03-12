// Get references to the color and size forms and buttons
const colorForm = document.getElementById("color-form");
const sizeForm = document.getElementById("size-form");
const addColorButton = document.getElementById("add-color-button");
const addSizeButton = document.getElementById("add-size-button");

// Add event listeners to the buttons
addColorButton.addEventListener("click", function () {
    colorForm.style.display = "block";
    sizeForm.style.display = "none";
    addColorButton.classList.remove('btn-secondary');
    addColorButton.classList.add('btn-primary');
    addSizeButton.classList.remove('btn-primary');
    addSizeButton.classList.add('btn-secondary');
});

addSizeButton.addEventListener("click", function () {
    colorForm.style.display = "none";
    sizeForm.style.display = "block";
    addSizeButton.classList.remove('btn-secondary');
    addSizeButton.classList.add('btn-primary');
    addColorButton.classList.remove('btn-primary');
    addColorButton.classList.add('btn-secondary');
});

// only alphanumeric and _
function onlyAlphanumericUnderscore(event) {
    var input = event.target;
    input.value = input.value.replace(/[^a-zA-Z0-9_]/g, '');
}
  