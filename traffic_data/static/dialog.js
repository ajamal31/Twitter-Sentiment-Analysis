$(document).ready(function () {
    $(document).on("click", ".get-url",function () {
        var url = $(this).attr('id');
            url = url.replace(/\s/g,"");
        var text = '<a href=' + url +'></a>';
        var feed = document.createElement("blockquote");
            feed.className = "twitter-tweet";
            feed.setAttribute("data-conversation", "none");
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
        $.getScript("/static/twitter_widget.js");

        $(".ui-widget-overlay").on("click", function(){
            $(".dial").dialog("close");
        });
    });
});
