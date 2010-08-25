window.addEvent('load', function() {
    $$('.link').addEvent('click', function() {
        var href = this.getProperty('href');
        window.location = href;
    });

    $$('.openlink').addEvent('click', function() {
        var href = this.getProperty('href');
        window.open(href);
    });

    $$('img.photographs', 'img.paintings', 'img.vinyl', 'img.illustrations').each(function(nav_img) {
        var size = nav_img.getSize();
        
        function doEnter(ev) {
            $(ev.target).morph({
                'top': [0, -20],
                'left': [0, -20],
                'height': [size.y, size.y + 40], 
                'width': [size.x, size.x + 40]
            });
        }
        
        function doLeave(ev) {
            $(ev.target).morph({
                'top': [-20, 0],
                'left': [-20, 0],
                'height': [size.y + 40, size.y], 
                'width': [size.x + 40, size.x]
            });
        }
        
        nav_img.addEvents({
            'mouseenter': doEnter,
            'mouseleave': doLeave
        });         
    });

    if ( $('my_slideshow') ) {
        var slideshow = new Slideshow(
            'my_slideshow', 
            data, 
            {
                loader: false, 
                captions: true, 
                height: 550, 
                width: 550, 
                controller: true, 
                thumbnails: true, 
                overlap: false, 
                resize: 'length', 
                linked: true, 
                delay: 3000, 
                paused: true,
                loop: true
            }
        );
    }
});

