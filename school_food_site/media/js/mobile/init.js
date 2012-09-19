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
    $('form').find('textarea, :input[type="date"], :input[type="password"], :input[type="text"], .ui-input-search')
        .removeClass('ui-body-a')
        .addClass('ui-body-b');

    window.mySwipe = new Swipe($('.photos').get(-1));
});

$(document).bind("mobileinit", function() {
    $.mobile.page.prototype.options.degradeInputs.date = true;
}); 
