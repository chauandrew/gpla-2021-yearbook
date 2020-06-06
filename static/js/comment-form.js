$('.comments-toggle').on('click', function (e) {
	// update hide/show comment section
	// TODO: add slide in/out animations
	e.preventDefault()
	commentsdiv = $(this).parent().siblings('.comments-collapse')
	if (commentsdiv.hasClass('hidden')) {
		$(this).children('.hide-toggle').removeClass("hidden")
		$(this).children('.unhide-toggle').addClass("hidden")
		commentsdiv.removeClass('hidden')
	} else {
		$(this).children('.hide-toggle').addClass("hidden")
		$(this).children('.unhide-toggle').removeClass("hidden")
		commentsdiv.addClass('hidden')
	}
})

$('.comment-form').on('submit', function (e) {
	e.preventDefault()

	postid = $(this).attr('id').replace('comment-form-', '')
	author = $(`#comment-author-${postid}`).val()
	body = $(`#comment-body-${postid}`).val()

	// only add if comment is not empty
	if (body) {
		if (!author) author = "Anonymous" // allow anon name
		body = author + ": " + body

		// add to comments, then ajax to server
		$(`#comments-${postid}`).append(`<li class="post-comment"><small>${body}</small></li>`)

		$.ajax({
			type: 'POST',
			url: '/comment',
			data: {
				postid: postid,
				body: body
			},
			success: function (message) {
				toastr.success(message)
			},
			error: function (message) {
				if (typeof message === 'string' || message instanceof String)
					toastr.warning(message)
				else
					toastr.warning("An unknown error has occured")
			}
		})

		// commented successfully, remove text from input
		$(`#comment-body-${postid}`).val('')
	}
})