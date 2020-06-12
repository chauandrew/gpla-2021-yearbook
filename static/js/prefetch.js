prefetched = []

// Prefetch urls the user hovers over
$('a:not([href^="#"])').on('mouseover', function() {
    var href = $(this).attr("href")
    if (prefetched.includes(href) || href.includes("/static/image")) {
        return;
    } else {
        prefetched.push(href)
    }
    let link = document.createElement("link");
    link.setAttribute("rel", "prefetch");
    link.setAttribute("href", href);
    document.head.appendChild(link);
});