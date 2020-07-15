// Infinite loading!
pageNum = 1;
finished = false;
mux = 0;

// Display more posts if available
function getPosts(page) {
    if (mux != 0) {
        return;
    }
    mux = 1;
    var args = { 'page': page };
    var request_url = '/api/posts/findall';
    $.ajax({
        type: 'POST',
        data: args,
        url: request_url,
        success: function (data) {
            var parsed = JSON.parse(data.replace(/(\r\n|\n|\r|\t)/gm, ""));
            if (parsed.length != 0) { // display more posts
                for (var i = 0; i < parsed.length; ++i) {
                    template = document.createElement('template');
                    template.innerHTML = parsed[i].replace(/(\r\n|\n|\r|\t)/gm, "").trim();
                    $('#post-wrapper').get(0).append(template.content.firstChild);
                }
                pageNum++;
            } else { // no more posts
                finished = true;
                loadposition = Infinity;
                $('#loading-spinner').hide();
            }
            mux = 0;
        },
        error: function (e) {
            console.log(`Could not load posts: ${e.responseText}`);
            toastr.warning(`Could not load more posts! Response: ${e.responseText}`);
            mux = 0;
        }
    });

    // temporary fix for comments not working for infinitely loaded posts

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
                url: '/api/posts/comment',
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
}

// on scroll, load new page
var loadposition = $('#loading-spinner').offset().top;
var scrollTimeout;
$(window).scroll(function () {
    if (scrollTimeout) {
        window.clearTimeout(scrollTimeout);
    }
    scrollTimeout = window.setTimeout(function () {
        if ((window.innerHeight + window.scrollY >= loadposition)) {
            if (!finished) {
                getPosts(pageNum);
            }
        }
    }, 250);
});
