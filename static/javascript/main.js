// Main application launcher
// Performs the following:

// 1) Configures Require.js for loading app resources.
// 2) Defines main application bootstrap (launcher) module.
// 3) Executes main module to launch the app.

// Application bootstrapper is responsible for:
// => Selecting and loading modules relevant to the current page.
// => Defining the shareable state of the current page.


// 1. File path config (relative to baseUrl):
requirejs.config({
    baseUrl: window.STATIC_ROOT + "/",
    paths: {
        "backbone": "libs/backbone",
        "jquery": "libs/jquery",
        "jquery.opentip": "libs/jquery.opentip",
        "underscore": "libs/underscore",
        "bootstrap": "libs/bootstrap"
    },
    shim: {
        "jquery.opentip": {
            deps: [ "jquery" ],
            exports: "$"
        }
    }
});


// 2. Main application bootstrapper:
define("main", function() {
    "use strict";

    // Bootstrapper:
    function bootstrap() {

        // Tests for an element by id.
        function has( id ) {
            return !!document.getElementById( id );
        }

        // Tests for an element with an attribute.
        function has_attr( attr ) {
            var items = document.getElementsByTagName("*");
            var items_len = items.length;
            for (var i = 0; i < items_len; i++) {
                if (items[i].hasAttribute(attr)) {
                    return true;
                }
            }
            return false;
        }

        // Tests for an element with a class name.
        function has_class( class_name ) {
            var items = document.getElementsByTagName("*");
            var items_len = items.length;
            var re = new RegExp("(?:^| )(" + class_name + ")(?: |$)");
            for (var i = 0; i < items_len; i++) {
                var item = items[i];
                if (item.hasAttribute("class") && re.test(item.getAttribute("class"))) {
                    return true;
                }
            }
            return false;

        }

        // Base modules:
        var mods = [];
        var id = "";

        // One-off application components...

        // Test for tooltips.
        if ( has_attr("data-ot") ) {
            mods.push( "jquery.opentip", "tooltips" );
        }

        // Test for filter form.
        if ( has_class("filtered-list") ) {
            mods.push( "filters" );
        }

        require( mods );


        return;


        // Test for debug mode:
        if ( window.djdt ) {
            mods.push( "common/debug-utils" );
        }

        // Test for snap header and/or related items:
        if ( has("fixed-toolbar") || has("related-items") ) {
            mods.push( "common/window-v" );
        }

        // Test for Selections application:
        if ( has("selections") ) {
            mods.push( "common/selections-v" );
        }

        // Test for page utilities:
        if ( has("page-utils") ) {
            mods.push( "common/page-utils-v" );
        }

        // Test for usertype survey:
        if ( has("usertype-survey") ) {
            mods.push( "common/usertype-survey-v" );
        }

        // Test for income preference selector:
        if ( has("income-preference") ) {
            mods.push( "common/income-pref-v" );
        }

        // Test for "find colleges" button w/ variable text:
        if ( has("find-colleges") ) {
            mods.push( "common/find-colleges-v" );
        }

        // Page-level applications...
        // Only one of the following may load per page.

        // => Home page test:
        if ( has("index-head") ) {
            mods.push( "pages/index-v", "common/share-mv" );
        }
        // => Search application test:
        else if ( has("search-results") ) {
            mods.push( "search/search-c" );
            id = "search";
        }
        // => College application test:
        else if ( has("school-detail") ) {
            mods.push( "college/college-v", "college/concepts-v" );
            id = "college";
        }
        // => Comparison application test:
        else if ( has("school-comparison") ) {
            mods.push( "compare/compare-v" );
            id = "compare";
        }

        // Define key application page IDs:
        define( "appId", id );

        // Require page components:
        require( mods );
    }

    // Allow module to return, then acquire JSON2 library if needed and bootstrap:
    if ( !window.JSON ) {
        require(["libs/json2"], bootstrap);
    } else {
        bootstrap();
    }
});


// 3. Require main to load application:
require(["main"]);
