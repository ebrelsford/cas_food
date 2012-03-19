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
                t.changeRating($(this), true);
            })
            .hover(
                function() {
                    t.changeRating($(this), false);
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

    changeRating: function($rating, pick) {
        this.changeArray($rating.prevAll('.rating'), true, pick);
        this.fill($rating);
        if (pick) {
            $rating.addClass('picked');
            // TODO something useful, AJAXy
        }
        this.changeArray($rating.nextAll('.rating'), false, pick);
    },

    resetRating: function() {
        this.changeRating(this.$elem.find('.picked'), true);
    }

};

$.plugin('rate', Rate);
