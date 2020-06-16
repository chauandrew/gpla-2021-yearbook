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
    var args = {'page': page};
    var request_url = '/api/posts/findall';
    $.ajax({
        type: 'POST',
        data: args,
        url: request_url,
        success: function(data) {
            var parsed = JSON.parse(data.replace(/(\r\n|\n|\r|\t)/gm, ""));
            if (parsed.length != 0) { // display more posts
                for (var i = 0; i < parsed.length; ++i) {
                    div = document.createElement('div');
                    div.innerHTML = parsed[i].replace(/(\r\n|\n|\r|\t)/gm, "");
                    $('#post-wrapper').get(0).append(div);
                }
                pageNum++;
            } else { // no more posts
                finished = true;
                loadposition = Infinity;
                $('#loading-spinner').hide();
            }
            mux = 0;
        },
        error: function(e) {
            console.log(`Could not load posts: ${e.responseText}`);
            toastr.warning(`Could not load more posts! Response: ${e.responseText}`);
            mux = 0;
        }
    });
}

// on scroll, load new page
var loadposition = $('#loading-spinner').offset().top;
var scrollTimeout;
$(window).scroll( function(){
    if(scrollTimeout) {
        window.clearTimeout(scrollTimeout);
    }
    scrollTimeout = window.setTimeout( function() {
        if ((window.innerHeight + window.scrollY >= loadposition)) {
            if (!finished) {
                getPosts(pageNum);
            }
        }
    }, 250);
});
