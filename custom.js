// custom.js
$(document).on('shiny:value', function(event) {
    setTimeout(function() {
        var imgHeight = $('.shiny-plot-output img').height();
        if (imgHeight) {
            $('.app-col').css('height', imgHeight + 50 + 'px');
        }
    }); 
});
