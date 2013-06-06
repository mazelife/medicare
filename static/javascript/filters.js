define(["jquery", "underscore"], function ( $, _ ) {

    var
        url = window.location.href,
        qs = window.location.search,
        form = $(".filtered-list form");

    // Clear the form and resumbmit when the "reset" button is clicked.
    $("button[type=reset]").click( function ( evt ) {
        evt.preventDefault();
        window.location.href = url.replace(qs, "");
    });

    // Submit the form when the enter key is pressed.
    $(document).ready(function () {
        $(document).keydown(function ( evt ) {
            if (evt.keyCode == 13) {
                evt.preventDefault();
                form.submit();
            }
        });
    });

});