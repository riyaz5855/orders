// script for increment and decrement button

// Get all buttons with dynamic IDs that contain "increment" or "decrement" in their IDs
const buttons = document.querySelectorAll('button[id*="increment"], button[id*="decrement"]');

// Loop through each button and add an event listener
buttons.forEach(function(button) {
  button.addEventListener('click', function() {
    // Get the ID of the button that was clicked
    const id = button.getAttribute('id');

    // Get the integer field with the same ID as the clicked button, by replacing "increment" or "decrement" with "integer-field"
    const integerField = document.getElementById(id.replace('increment', 'integer-field').replace('decrement', 'integer-field'));

    // Increase or decrease the value of the integer field, depending on which button was clicked
    if (id.includes('increment')) {
      integerField.value = parseInt(integerField.value) + 1;
    } else {
      if (parseInt(integerField.value) > 0) {
        integerField.value = parseInt(integerField.value) - 1;
      }
    }
  });
});


// image view

// Get all images with class "sml"
const images = document.querySelectorAll('.sml');

// Loop through each image and add event listener
images.forEach(image => {
  image.addEventListener('click', () => {
    // Get the src of the clicked image and store it in x
    const x = image.getAttribute('src');
    
    // Find the image with id "mainImage"
    const mainImage = document.getElementById('mainImage');
    
    // Change the src of mainImage to x
    mainImage.setAttribute('src', x);
  });
});


// prevent submit if quantity is zero
const form = document.querySelector('form'); // select the form element
const quantInputs = form.querySelectorAll('.quant'); // select all input elements with class name 'quant'

form.addEventListener('submit', function(e) {
  // prevent form submission if all 'quant' input fields have value 0
  const allZeros = Array.from(quantInputs).every(input => input.value === '0');
  if (allZeros) {
    e.preventDefault();
    alert('Please select some quantities.');
  }
});
