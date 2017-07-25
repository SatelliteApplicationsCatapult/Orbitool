var panels = panels || {};
panels.Accordion = function() {
    this.panels = [];
};
panels.Accordion.prototype = {
    makePanel: function(panelElement) {
        var panel = new panels.AccordionPanel(panelElement,this);
        this.panels.push(panel);
    }
};
panels.AccordionPanel = function(el, panelHolder) {
    var self = this;
    this.el = el;
    this.mb = $(el).find('.panel-button').get();
    this.isSelected = false;
    $(el).find('.accordion-panel__heading').on('click', function() {
        if (self.isSelected) {
            self.unselect();
        } else {
            self.select();
        }
    });
    return this;
};
panels.AccordionPanel.prototype = {
    select: function() {
        $(this.el).addClass('active');
        $(this.mb).addClass('open-menu');
        this.isSelected = true;
    },
    unselect: function() {
        $(this.el).removeClass('active');
        $(this.mb).removeClass('open-menu');
        this.isSelected = false;
    }
};
panels.init = function() {
    var self = this;
    this.accordionContainer = new panels.Accordion();
    $('.accordion-panel').iterate(function(el){
        self.accordionContainer.makePanel(el);
    });
    // this.accordionContainer.panels[1].select();
};
function setMargins() {
    var sw = screen.availWidth;
    var w = document.body.clientWidth;
    var h = window.innerHeight;

    var huse = h*(0.1-((((sw-w)/sw)/10)*1.25));
    huse = (huse < 32 ? 32 : huse);

    $('#content').css('padding', huse+'px');

    var hH = $('header').css('height', huse+'px').height();
    $('header').css('height', '5px').css('transition','0.2s').css('overflow','hidden').on('mouseover', function(){
        $('header').css('height', huse+'px');
        var nTH = $('#navToggle').css('top',huse+'px').height();
        $('#mainNav').css('top', huse+nTH+'px');
    }).on('mouseout', function(){
        $('header').css('height', '5px');
        var nTH = $('#navToggle').css('top','5px').height();
        $('#mainNav').css('top', 5+nTH+'px');
    });

    $('.menu-logo, .menu-button, .menu-logo > svg, .menu-button svg').css('height', hH+'px');

    var cW = $('#menu-bar > div').width(true);

    // var cW = menuBar.width();
    var lM = (w>cW ? (w-cW)/2 : 0);
    $('#menu-bar').css('marginLeft', lM+'px').css('min-width', cW+200+'px');

    var nTH = $('#navToggle').css('top','5px').height();
    $('#mainNav').css('top', 5+nTH+'px');
}
$.ready(function() {
    setMargins();
    window.addEventListener('resize', function(event){
        setMargins();
    }, true);
    $('#mainNav').addClass('collapsed');
    $('#navToggle').on('click', function () {
        $('#mainNav').toggleClass('collapsed');
        this.innerHTML = this.innerHTML === "+" ? "-" : "+";
    });
    panels.init();
    $('html').css('visibility', 'visible');
});