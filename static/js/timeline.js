// add smooth scrolling to local hrefs
$(document).ready(function ($) {
    $('a[href^="#event"]').bind('click.smoothscroll', function (e) {
        var target = this.hash,
            $target = $(target);

        $('html, body').animate({
            'scrollTop': $target.offset().top - 50
        }, 900, 'swing', function () {
            window.location.hash = target;
        });
    });
});

// animate in sidebar circles when we reach certain location on page
$(document).scroll(function () {
    var y = $(this).scrollTop();
    if (y > 250) {
        $('.sidebar').fadeIn();
    } else {
        $('.sidebar').fadeOut();
    }
});