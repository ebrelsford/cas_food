function every_page_load() {
    $('.rate').rate({
        loggedIn: casfood_state.authenticated,
        $logInDialog: $('#log-in-dialog'),
    });

    $(':input.date.no-future').datepicker('option', 'maxDate', '+0');
}

if (!casfood_state.mobile) {
    $(document).ready(function() {
        every_page_load();
    });
}
else {
    $(document).on('pageinit', function() {
        every_page_load();
    });
}
