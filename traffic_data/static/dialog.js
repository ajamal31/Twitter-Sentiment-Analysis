$(document).ready(function () {
    $(document).on("click", ".get-url",function (e) {
        e.preventDefault();
        var id = $(this).attr('id');
        var feed = document.createElement("blockquote");
            feed.className = "twitter-tweet";
            feed.innerHTML =  '<a href=' + id + '></a>'
            + '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>';
        $(".dial").html(feed);
        $(".dial").dialog({
            title: "Tweet",
            draggable: false,
            position: {my: "center", at: "top"},
            modal: true,
            minHeight: 200,
            minWidth: 500,
            dialogClass: 'dial-head'
        });
    });
});
