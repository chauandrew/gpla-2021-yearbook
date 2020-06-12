// Preload next couple images in carousel when user hovers over / clicks on next arrow
var images=[];
function preload(urls) {
    for (var i = 0; i < urls.length; i++) {
        images[i] = new Image();
        images[i].src = urls[i];
    }
}

var preloaded = [];
$('.carousel-control-next').on('mouseover click', function() {
	var slideid = $('.carousel-item.active').attr('id').replace("carousel-slide-", "");
	slideid = Number(slideid) + 1
	var imgurls = []
	var n = $('.carousel-item').length
	for (var i = 0; i < 3; i++) { 
		var id = slideid + i % n;
		if (!preloaded.includes(id)) {
			console.log("preloading", id)
			preloaded.push(id);
			imgurls.push($(`#carousel-slide-${id}`).children('img').attr('src'));
		}
	}
	preload(imgurls);
});

