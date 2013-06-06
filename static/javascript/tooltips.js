define(["jquery"], function ( $ ) {

    $("*[data-ot]")
        .wrapInner('<span class="tt">')
        .append('<span class="tt-indicator"></span>');

    return {};
});