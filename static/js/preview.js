function setMargins() {
    var sw = screen.availWidth;
    var w = document.body.clientWidth;
    var h = window.innerHeight;

    // var huse = h*(0.1-((((sw-w)/sw)/10)*1.25));
    var huse = h*(0.1-((((sw-w)/sw)/10)));
    huse = (huse < 32 ? 32 : huse);

    $('#content').css('padding-top', huse+'px');

    var hH = $('header').css('height', huse+'px').height();

    $('.menu-logo, .menu-button, .menu-logo > svg, .menu-button svg').css('height', hH+'px');
    $('.feature-image').css('height', hH*2+'px');

    var cW = $('#menu-bar > div').width(true);

    // var cW = menuBar.width();
    var lM = (w>cW ? (w-cW)/2 : 0);
    // $('#menu-bar').css('marginLeft', lM+'px').css('marginTop', (hH-mH)/2+'px').css('min-width', cW+200+'px');
    $('#menu-bar').css('marginLeft', lM+'px').css('min-width', cW+200+'px');

}

$.ready(function() {
    setMargins();
    window.addEventListener('resize', function(event){
        setMargins();
    }, true);
    $('html').css('visibility','visible');
});