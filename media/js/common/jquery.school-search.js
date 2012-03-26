var SchoolSearch = {
    options: {
        geocode_url: '/geo/geocode',
        map_id: 'map',
        autocomplete: true,
        mobile: false,
    },

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);
        this.mapObj = $('#' + this.options.map_id).data('schoolmap');
        this.$schoolInput = this.$elem.find(':input[name="school"]');
        this.$submit = this.$elem.find(':input[type="submit"]');

        var t = this;

        if (t.options.autocomplete) {
            this.$schoolInput.on('autocompleteselect', function(e, ui) {
                $(this).data('current_school', { 
                    id: ui.item.id,
                    name: ui.item.value,
                });
                t.zoomToSchool(ui.item.id);
            });
        }

        this.$elem.submit(function(e) {
            e.preventDefault();

            var input = t.$schoolInput.val();

            if (t.options.autocomplete) {
                // had already selected a school, just select that again if the input hasn't changed
                var current_school = t.$schoolInput.data('current_school');
                if (current_school && current_school.name === input) {
                    this.zoomToSchool(current_school.id);
                    return;
                }
            }

            // search by address
            t.$elem.find('.loading').addClass('active');
            $.getJSON(t.options.geocode_url + '?location=' + input, 
                function(data) { 
                    t.$elem.find('.loading').removeClass('active');
                    if (t.options.mobile) {
                        t.$submit.parents('.ui-btn').hide();
                    }
                    if (data) {
                        t.mapObj.centerOnLonLat(data.longitude, data.latitude, true);
                        t.$elem.find('.error-message').text('');
                    }
                    else {
                        t.$elem.find('.error-message').text("Couldn't find the address you entered. Be more specific?");
                    }
                }
            );

            if (t.options.mobile) {
                t.$submit.parents('.ui-btn').hide();
                t.$schoolInput.focus(function() {
                    t.$submit.parents('.ui-btn').show();
                });
                t.$schoolInput.keypress(function() {
                    t.$submit.parents('.ui-btn').show();
                });
            }

            return false;
        });
    },

    zoomToSchool: function(id) {
        this.mapObj.zoomToFid(id, true);
    },

};

$.plugin('schoolsearch', SchoolSearch);
