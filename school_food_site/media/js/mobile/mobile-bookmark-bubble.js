window.addEventListener('load', function() {
    window.setTimeout(function() {
        var bubble = new google.bookmarkbubble.Bubble();

        var parameter = 'NOT USED';

        bubble.hasHashParameter = function() {
            // intentionally do nothing
            return false;
        };

        bubble.setHashParameter = function() {
            // intentionally do nothing
        };

        /*
         * Override build_ to change text, theoretically styling too.
         */
        bubble.build_ = function() {
            var bubble = document.createElement('div');
            var isIpad = this.isIpad_();

            bubble.style.position = 'absolute';
            bubble.style.zIndex = 1000;
            bubble.style.width = '100%';
            bubble.style.left = '0';
            bubble.style.top = '0';

            var bubbleInner = document.createElement('div');
            bubbleInner.style.position = 'relative';
            bubbleInner.style.width = '214px';
            bubbleInner.style.margin = isIpad ? '0 0 0 82px' : '0 auto';
            bubbleInner.style.border = '2px solid #fff';
            bubbleInner.style.padding = '20px 20px 20px 10px';
            bubbleInner.style.WebkitBorderRadius = '8px';
            bubbleInner.style.WebkitBoxShadow = '0 0 8px rgba(0, 0, 0, 0.7)';
            bubbleInner.style.WebkitBackgroundSize = '100% 8px';
            bubbleInner.style.backgroundColor = '#b0c8ec';
            bubbleInner.style.background = '#cddcf3 -webkit-gradient(linear, ' +
                'left bottom, left top, ' + isIpad ?
                    'from(#cddcf3), to(#b3caed)) no-repeat top' :
                    'from(#b3caed), to(#cddcf3)) no-repeat bottom';
            bubbleInner.style.font = '13px/17px sans-serif';
            bubble.appendChild(bubbleInner);

            // The "Add to Home Screen" text is intended to be the exact same text
            // that is displayed in the menu of Mobile Safari.
            // 
            // This was changed from the original to refer to Lunch Line.
            if (this.getIosVersion_() >= this.getVersion_(4, 2)) {
                bubbleInner.innerHTML = 'Install Lunch Line on your phone: ' +
                  'tap on the arrow and then <b>\'Add to Home Screen\'</b>';
            } else {
                bubbleInner.innerHTML = 'Install Lunch Line on your phone: ' +
                    'tap <b style="font-size:15px">+</b> and then ' +
                    '<b>\'Add to Home Screen\'</b>';
            }

            var icon = document.createElement('div');
            icon.style['float'] = 'left';
            icon.style.width = '55px';
            icon.style.height = '55px';
            icon.style.margin = '-2px 7px 3px 5px';
            icon.style.background =
                '#fff url(' + this.getIconUrl_() + ') no-repeat -1px -1px';
            icon.style.WebkitBackgroundSize = '57px';
            icon.style.WebkitBorderRadius = '10px';
            icon.style.WebkitBoxShadow = '0 2px 5px rgba(0, 0, 0, 0.4)';
            bubbleInner.insertBefore(icon, bubbleInner.firstChild);

            var arrow = document.createElement('div');
            arrow.style.backgroundImage = 'url(' + this.IMAGE_ARROW_DATA_URL_ + ')';
            arrow.style.width = '25px';
            arrow.style.height = '19px';
            arrow.style.position = 'absolute';
            arrow.style.left = '111px';
            if (isIpad) {
                arrow.style.WebkitTransform = 'rotate(180deg)';
                arrow.style.top = '-19px';
            } else {
                arrow.style.bottom = '-19px';
            }
            bubbleInner.appendChild(arrow);

            var close = document.createElement('a');
            close.onclick = google.bind(this.closeClickHandler_, this);
            close.style.position = 'absolute';
            close.style.display = 'block';
            close.style.top = '-3px';
            close.style.right = '-3px';
            close.style.width = '16px';
            close.style.height = '16px';
            close.style.border = '10px solid transparent';
            close.style.background =
                'url(' + this.IMAGE_CLOSE_DATA_URL_ + ') no-repeat';
            bubbleInner.appendChild(close);

            return bubble;
        };

        bubble.getViewportHeight = function() {
            return window.innerHeight;
        };

        bubble.getViewportScrollY = function() {
            return window.pageYOffset;
        };

        bubble.registerScrollHandler = function(handler) {
            window.addEventListener('scroll', handler, false);
        };

        bubble.deregisterScrollHandler = function(handler) {
            window.removeEventListener('scroll', handler, false);
        };

        bubble.showIfAllowed();
  }, 1000);
}, false);
