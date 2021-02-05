$(document).ready(function() {
    setTimeout(hide_errors, 10000);

    function hide_errors() {
        $('#error_wrapper').slideUp();
    }

    let new_pin_value
    $('.keypad-button').click(function(e) {
        e.preventDefault();
        let current_pin_value = $("#pin").val();
        let value = $(this).data('value');
        if(value !== 'x') {
            new_pin_value = current_pin_value + value;
        } else {
            new_pin_value = current_pin_value.substring(0, current_pin_value.length - 1);
        }
        $('#pin').val(new_pin_value);
    });
});
