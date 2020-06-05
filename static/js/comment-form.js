$('.comment-form').on('submit', function (e) {
	e.preventDefault()

	postid = $(this).attr('id').replace('comment-form-', '')
	body = $(`#comment-input-${postid}`).val()

	// only add if comment is not empty
	if (body) {
		// add to comments, then ajax to server
		$(`#comments-${postid}`).append(`<li class="list-group-item post-comment">${body}</li>`)

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
		$(`#comment-input-${postid}`).val('')
	}
})