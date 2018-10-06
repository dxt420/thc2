(function ($) {
    'use strict';





    //========================
    // Loader 
    //========================
    $(window).load(function () {
        if ($('.preloader').length > 0) {
            $('.preloader').delay(800).fadeOut('slow');
        }
    });


})(jQuery);
