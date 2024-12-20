// script for size and price
$('input[type="checkbox"]').change(function () {
    var checkboxId = $(this).attr('id');
    var inputId = 'input-' + checkboxId.split('-')[1];
    if ($(this).is(':checked')) {
      $('#' + inputId).removeClass('hidden-input');
      $('#' + inputId).prop('required',true);
    } else {
      $('#' + inputId).addClass('hidden-input');
      $('#' + inputId).prop('required',false);
      $('#' + inputId).val(''); // set input value to empty string
    }
});

// script for image preview
function readFile(input) {
    $("#status").html('Processing...');
    $("#photos").empty();
    counter = input.files.length;
    for (x = 0; x < counter; x++) {
    if (input.files && input.files[x]) {

        var reader = new FileReader();

        reader.onload = function (e) {
        $("#photos").append('<div class="col-md-3 col-sm-3 col-xs-3"><img src="' + e.target.result + '" class="img-thumbnail"></div>');
        };

        reader.readAsDataURL(input.files[x]);
    }
    }
    if (counter == x) { $("#status").html(''); }
}


// only alphanumeric and _
function onlyAlphanumericUnderscore(event) {
  var input = event.target;
  input.value = input.value.replace(/[^a-zA-Z0-9_]/g, '');
}