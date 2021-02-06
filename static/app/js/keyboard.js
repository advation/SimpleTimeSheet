let uppercase = false;
let selected_field = $('input').first().focus();

$('input').focus(function() {
    selected_field = $(this);
});

$('#shift-key').click(function() {
    if(uppercase === false) {
        $(this).removeClass('bg-light text-dark');
        $(this).addClass('bg-secondary text-light');
        uppercase = true;
        $('.keyboard-key').each(function() {
            let v = $(this).text();
            if(v !== "Space")
            {
                $(this).text(v.toUpperCase());
            }
        });
    }
    else
    {
        $(this).removeClass('bg-secondary text-light');
        $(this).addClass('bg-light text-dark');
        uppercase = false;
        $('.keyboard-key').each(function() {
            let v = $(this).text();
            if(v !== "Space")
            {
                $(this).text(v.toLowerCase());
            }
        });
    }
});

$('#back-key').click(function() {
    let old_value = selected_field.val();
    let new_value = old_value.substring(0, old_value.length - 1);
    selected_field.val(new_value);
});

$('.keyboard-key').click(function(e) {
    e.preventDefault();
    let value = $(this).data('value');
    let old_value = selected_field.val();
    if(uppercase === true) {
        if(!parseInt(value)) {
            if(value !== 0) {
                value = value.toUpperCase();
            }
        }
    }
    else {
        if(!parseInt(value)) {
            if(value !== 0) {
                value = value.toLowerCase()
            }
        }
    }
    let new_value = old_value + value;
    selected_field.val(new_value);
});