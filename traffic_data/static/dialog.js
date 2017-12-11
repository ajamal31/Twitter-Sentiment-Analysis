$(document).ready(function () {
    $(document).on("click", ".get-url",function (e) {
        e.preventDefault();
        var url = $(this).attr('id');
        url = url.replace(/\s/g,"");
        var text = '<a href=' + url +'></a>' + '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>';
        var feed = document.createElement("blockquote");
            feed.className = "twitter-tweet";
            feed.innerHTML =  text;
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
        $(".ui-widget-overlay").on("click", function(){
            $(".dial").dialog("close");
        });
    });
});
