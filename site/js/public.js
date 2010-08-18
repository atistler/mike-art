window.addEvent('domready', function() {
	$$('.link').addEvent('click', function() {
		var href = this.getProperty('href');
		window.location = href;
	});

	$$('.openlink').addEvent('click', function() {
		var href = this.getProperty('href');
		window.open(href);
	});	
});

