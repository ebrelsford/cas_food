//
// A photo pager
//

var PhotoPager = {
    options: {
        baseUrl: '',    // url to fetch photos from
        count: 1,       // number to move back/ahead by XXX only 1 will work as is
        index: 0,       // index to start at (counting from the most recent)
        cycle: true,    // ensure even/odd cycling
        $listContainer: null,           // container new photos will be added to
        elementClass: '',               // class of elements added to container
        onMove: function(photos) {},      // callback on moving either direction
        onPrevious: function(photos) {},  // callback on moving back
        onNext: function(photos) {},      // callback on moving forward
    },

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);

        this.baseUrl = this.options.baseUrl;
        this.index = this.options.index;
        this.count = this.options.count;
        this.cycle = this.options.cycle;
        this.$listContainer = this.options.$listContainer;
        this.elementClass = this.options.elementClass;
        this.onMove = this.options.onMove;
        this.onPrevious = this.options.onPrevious;
        this.onNext = this.options.onNext;

        var t = this;
        this.$elem.find('.previous').click(function() {
            t.previous();
        });

        this.$elem.find('.next').click(function() {
            t.next();
        });
    },

    move: function(amount, callback) {
        var t = this;
        this.index += amount;

        if (amount < 0) {
            var $already_loaded = this._getPreviousAlreadyLoaded();
            if ($already_loaded.length) {
                this._getVisiblePhotos().eq(-1).hide()
                $already_loaded.eq(-1).show();
                return;
            }
        }
        if (amount > 0) {
            var $already_loaded = this._getNextAlreadyLoaded();
            if ($already_loaded.length) {
                this._getVisiblePhotos().eq(0).hide()
                $already_loaded.eq(0).show();
                return;
            }
        }
        $.get(this.baseUrl + '?',
            {
                count: this.count,
                index: this.index,
            },
            function(photos) {
                // could animate if we wanted to
                // TODO check if previous/next buttons should be disabled
                if (photos.trim() !== '') {
                    callback(photos);
                    t.onMove(photos);
                }
                else {
                    // fix the index!
                    t.index -= amount;
                }
            }
        );
    },

    previous: function() {
        var t = this;
        this.move(-t.count, function(photos) {
            // make room for new photos
            t._getVisiblePhotos().eq(-1).hide()

            // add new photos
            t.$listContainer.prepend(photos);

            // cycle classes
            if (t.cycle) {
                var $visible = t._getVisiblePhotos();
                t.addCycleClass($visible.eq(1), $visible.eq(0));
            }

            t.onPrevious(photos);
        });
    },

    next: function() {
        var t = this;
        this.move(+t.count, function(photos) {
            // make room for new photos
            t._getVisiblePhotos().eq(0).hide()

            // add new photos
            t.$listContainer.append(photos);

            // cycle
            if (t.cycle) {
                var $visible = t._getVisiblePhotos();
                t.addCycleClass($visible.eq(-2), $visible.eq(-1));
            }

            t.onNext(photos);
        });
    },

    _getPreviousAlreadyLoaded: function() {
        return this._getVisiblePhotos().eq(0).prev();
    },

    _getNextAlreadyLoaded: function() {
        return this._getVisiblePhotos().eq(-1).next();
    },

    _getVisiblePhotos: function() {
        return this.$listContainer.find('li.' + this.elementClass + ':visible');
    },

    //
    // Add cycle class to new photo based on its adjacent photo
    //
    addCycleClass: function($adjacent_photo, $new_photo) {
        var adjacent_photo_classes = $adjacent_photo.attr('class').split(' ');
        var new_photo_class = (adjacent_photo_classes.indexOf('odd') >= 0) ?
            'even': 'odd';
        $new_photo
            .removeClass('odd even')
            .addClass(new_photo_class);
    },
};

$.plugin('photopager', PhotoPager);
