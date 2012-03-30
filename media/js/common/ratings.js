var Rate = {
    options: {
    },

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);

        var t = this;
        this.$elem.find('.rating')
            .click(function() {
                t.changeRating($(this), true, true);
            })
            .hover(
                function() {
                    t.changeRating($(this), false, false);
                },
                function() { 
                    t.resetRating();
                }
            );
    },

    fill: function($rating) {
        $rating.removeClass('empty');
        $rating.addClass('full');
    },

    empty: function($rating) {
        $rating.removeClass('full');
        $rating.addClass('empty');
    },

    changeArray: function($ratingArray, fill, pick) {
        var t = this;
        $ratingArray.each(function() {
            if (pick) {
                $(this).removeClass('picked');
            }

            if (fill) {
                t.fill($(this));
            }
            else {
                t.empty($(this));
            }
        });
    },

    changeRating: function($rating, pick, clicked) {
        this.changeArray($rating.prevAll('.rating'), true, pick);
        this.fill($rating);
        if (pick) {
            $rating.addClass('picked');
            if (clicked) {
                var points = $rating.prevAll('.rating').length + 1;
                this.onChangeRating(points);
            }
        }
        this.changeArray($rating.nextAll('.rating'), false, pick);
    },

    resetRating: function() {
        this.changeRating(this.$elem.find('.picked'), true, false);
    },

    onChangeRating: function(points) {
        var $wrapper = this.$elem.parent();
        var $loading = $wrapper.find('.loading');
        $loading.show();
        $.getJSON(this.$elem.data('change-rating-url'), { 'points': points },
            function(data) {
                $loading.hide();
                if (data.status === 'OK') {
                    $wrapper.find('.ratings-average').text(data.average);
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
