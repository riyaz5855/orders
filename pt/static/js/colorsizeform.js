// Get references to the color and size forms and buttons
const colorForm = document.getElementById("color-form");
const sizeForm = document.getElementById("size-form");
const categoryForm = document.getElementById("category-form");
const addColorButton = document.getElementById("add-color-button");
const addSizeButton = document.getElementById("add-size-button");
const addCategoryButton = document.getElementById("add-category-button");



// Add event listeners to the buttons
addColorButton.addEventListener("click", function () {
    colorForm.style.display = "block";
    sizeForm.style.display = "none";
    categoryForm.style.display = "none";
    addColorButton.classList.remove('btn-secondary');
    addColorButton.classList.add('btn-primary');
    addSizeButton.classList.remove('btn-primary');
    addSizeButton.classList.add('btn-secondary');
    addCategoryButton.classList.remove('btn-primary');
    addCategoryButton.classList.add('btn-secondary');
});

addSizeButton.addEventListener("click", function () {
    colorForm.style.display = "none";
    sizeForm.style.display = "block";
    categoryForm.style.display = "none";
    addSizeButton.classList.remove('btn-secondary');
    addSizeButton.classList.add('btn-primary');
    addColorButton.classList.remove('btn-primary');
    addColorButton.classList.add('btn-secondary');
    addCategoryButton.classList.remove('btn-primary');
    addCategoryButton.classList.add('btn-secondary');
});

addCategoryButton.addEventListener("click", function () {
    colorForm.style.display = "none";
    sizeForm.style.display = "none";
    categoryForm.style.display = "block";
    addCategoryButton.classList.remove('btn-secondary');
    addCategoryButton.classList.add('btn-primary');
    addColorButton.classList.remove('btn-primary');
    addColorButton.classList.add('btn-secondary');
    addSizeButton.classList.remove('btn-primary');
    addSizeButton.classList.add('btn-secondary');
});

// only alphanumeric and _
function onlyAlphanumericUnderscore(event) {
    var input = event.target;
    input.value = input.value.replace(/[^a-zA-Z0-9_]/g, '');
}
  