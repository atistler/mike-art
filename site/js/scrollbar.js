	var ScrollBar = new Class({

		Implements: [Events, Options],

		options: {
			maxThumbSize: 10,
			wheel: 8
		},

		initialize: function(content, track, thumb, options){
			this.setOptions(options);

			this.content = $(content);
			this.track = $(track);
			this.thumb = $(thumb);

			this.bound = {
				'start': this.start.bind(this),
				'end': this.end.bind(this),
				'drag': this.drag.bind(this),
				'wheel': this.wheel.bind(this),
				'page': this.page.bind(this)
			};

			this.position = {};
			this.mouse = {};
			this.update();
			this.attach();
		},

		update: function(){

			this.contentSize = this.content.offsetHeight;
			this.contentScrollSize = this.content.scrollHeight;
			this.trackSize = this.track.offsetHeight;

			this.contentRatio = this.contentSize / this.contentScrollSize;

			this.thumbSize = (this.trackSize * this.contentRatio).limit(this.options.maxThumbSize, this.trackSize);

			this.scrollRatio = this.contentScrollSize / this.trackSize;

			this.thumb.setStyle('height', this.thumbSize);

			this.updateThumbFromContentScroll();
			this.updateContentFromThumbPosition();
		},

		updateContentFromThumbPosition: function(){
			this.content.scrollTop = this.position.now * this.scrollRatio;
		},

		updateThumbFromContentScroll: function(){
			this.position.now = (this.content.scrollTop / this.scrollRatio).limit(0, (this.trackSize - this.thumbSize));
			this.thumb.setStyle('top', this.position.now);
		},

		attach: function(){
			this.thumb.addEvent('mousedown', this.bound.start);
			if (this.options.wheel) this.content.addEvent('mousewheel', this.bound.wheel);
			this.track.addEvent('mouseup', this.bound.page);
		},

		wheel: function(event){
			this.content.scrollTop -= event.wheel * this.options.wheel;
			this.updateThumbFromContentScroll();
			event.stop();
		},

		page: function(event){
			if (event.page.y > this.thumb.getPosition().y) this.content.scrollTop += this.content.offsetHeight;
			else this.content.scrollTop -= this.content.offsetHeight;
			this.updateThumbFromContentScroll();
			event.stop();
		},

		start: function(event){
			this.mouse.start = event.page.y;
			this.position.start = this.thumb.getStyle('top').toInt();
			document.addEvent('mousemove', this.bound.drag);
			document.addEvent('mouseup', this.bound.end);
			this.thumb.addEvent('mouseup', this.bound.end);
			event.stop();
		},

		end: function(event){
			document.removeEvent('mousemove', this.bound.drag);
			document.removeEvent('mouseup', this.bound.end);
			this.thumb.removeEvent('mouseup', this.bound.end);
			event.stop();
		},

		drag: function(event){
			this.mouse.now = event.page.y;
			this.position.now = (this.position.start + (this.mouse.now - this.mouse.start)).limit(0, (this.trackSize - this.thumbSize));
			this.updateContentFromThumbPosition();
			this.updateThumbFromContentScroll();
			event.stop();
		}

	});


