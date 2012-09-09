$(document).on('pageshow', '#map-page', function(event) {
    $('#map-page #map').height($(window).height() - $('#map-page [data-role="header"]').height())
    $('#map').schoolmap({
        boroughs: 'Brooklyn,Manhattan',   
        types: 'Elementary',
        mobile: true,
    });
    $('form.school-search').schoolsearch({
        autocomplete: false,   
        mobile: true,
    });
});

$(document).on('pageinit', function() {
    $('form textarea, form :input[type="text"]')
        .removeClass('ui-body-a')
        .addClass('ui-body-b');
});
