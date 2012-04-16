//
// Simple up/down ratings.
//

var Rate = {
    options: {
        $logInDialog: null,
        loggedIn: false,
        requireLogin: true,
    },

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);

        var t = this;
        this.$elem.find('.rating')
            .click(function() {
                if (t.options.requireLogin && !t.options.loggedIn) {
                    // force login
                    if (t.options.$logInDialog !== null) {
                        t.options.$logInDialog.dialog('open');
                    }
                }
                else {
                    t.changeRating($(this));
                }
            });
    },

    clearRatings: function() {
        this.$elem.find('.rating').removeClass('picked');
    },

    changeRating: function($rating) {
        this.clearRatings();
        $rating.addClass('picked');
        this.onChangeRating($rating.data('rating-points'));
    },

    onChangeRating: function(points) {
        var $wrapper = this.$elem.parent();
        var $loading = $wrapper.find('.loading');
        $loading.show();
        $.getJSON(this.$elem.data('change-rating-url'), { 'points': points },
            function(data) {
                $loading.hide();
                if (data.status === 'OK') {
                    $wrapper.find('.ratings-sum').text(data.sum);
                    $wrapper.find('.ratings-count').text(data.count);
                    $wrapper.find('.ratings-plural').text(data.count !== 1 ? 's' : '');
                    $wrapper.find('.ratings-results').show();
                }
                else {
                    console.log('failure');
                }
            }
        );
    },

};

$.plugin('rate', Rate);
