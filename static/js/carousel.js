// Preload next couple images in carousel when user hovers over / clicks on next arrow
var images=[];
function preload(urls) {
    for (var i = 0; i < urls.length; i++) {
        images[i] = new Image();
        images[i].src = urls[i];
    }
}

var preloaded = [];
var timeout;
$('.carousel-control-next').on('mouseover click', function() {
	if (timeout) {
		window.clearTimeout(timeout);
	}
	timeout = window.setTimeout( function() {
		var imgurls = []
		try {
			next = $(this).parent().find('.active').next();
			id = next.attr('id').replace("#carousel", "").replace("slide", "");
			if (!preloaded.includes(id)) {
				preloaded.push(id)
				imgurls.push(next.children('img').attr('src'));
			} 
			next2 = next.next()
			id2 = next2.attr('id').replace("#carousel", "").replace("slide", "");
			if (!preloaded.includes(id2)) {
				preloaded.push(id2)
				imgurls.push(next2.children('img').attr('src'));
			} 
		} catch {}
		console.log(imgurls);
		preload(imgurls);
	}.bind(this), 100);
});
