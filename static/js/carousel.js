// sync descriptions with slides

$('#carousel').on('slid.bs.carousel', function (e) {

	// get slide index of current slide
	slideid = $('.carousel-item.active').attr('id').replace("carousel-slide-", "")

	console.log(`slide ${slideid}`)

	// hide all captions, then show caption corresponding to current slide
	$('.slide-caption').map(function (e) {
		if (!$(this).hasClass('hidden')) {
			$(this).addClass('hidden')
		}
	})
	$(`#slide-caption-${slideid}`).removeClass('hidden')
})