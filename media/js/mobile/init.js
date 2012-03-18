$(document).on('pageshow', '#map-page', function(event) {
    $('#map-page #map').height($(window).height() - $('#map-page [data-role="header"]').height())
    $('#map').schoolmap({
        boroughs: 'Brooklyn,Manhattan',   
        types: 'Elementary',
        mobile: true,
    });
});
