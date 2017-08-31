// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.

// Label Better
// https://github.com/peachananr/label_better
//!function(e){var t={position:"top",animationTime:500,easing:"ease-in-out",offset:20,hidePlaceholderOnFocus:true};e.fn.animateLabel=function(t,n){var r=n.data("position")||t.position,i=0,s=0;e(this).css({left:"auto",right:"auto",position:"absolute","-webkit-transition":"all "+t.animationTime+"ms "+t.easing,"-moz-transition":"all "+t.animationTime+"ms "+t.easing,"-ms-transition":"all "+t.animationTime+"ms "+t.easing,transition:"all "+t.animationTime+"ms "+t.easing});switch(r){case"top":i=0;s=(e(this).height()+t.offset)*-1;e(this).css({top:"0",opacity:"1","-webkit-transform":"translate3d("+i+", "+s+"px, 0)","-moz-transform":"translate3d("+i+", "+s+"px, 0)","-ms-transform":"translate3d("+i+", "+s+"px, 0)",transform:"translate3d("+i+", "+s+"px, 0)"});break;case"bottom":i=0;s=e(this).height()+t.offset;e(this).css({bottom:"0",opacity:"1","-webkit-transform":"translate3d("+i+", "+s+"px, 0)","-moz-transform":"translate3d("+i+", "+s+"px, 0)","-ms-transform":"translate3d("+i+", "+s+"px, 0)",transform:"translate3d("+i+", "+s+"px, 0)"});break;case"left":i=(e(this).width()+t.offset)*-1;s=0;e(this).css({left:0,top:0,opacity:"1","-webkit-transform":"translate3d("+i+"px, "+s+"px, 0)","-moz-transform":"translate3d("+i+"px, "+s+"px, 0)","-ms-transform":"translate3d("+i+"px, "+s+"px, 0)",transform:"translate3d("+i+"px, "+s+"px, 0)"});break;case"right":i=e(this).width()+t.offset;s=0;e(this).css({right:0,top:0,opacity:"1","-webkit-transform":"translate3d("+i+"px, "+s+"px, 0)","-moz-transform":"translate3d("+i+"px, "+s+"px, 0)","-ms-transform":"translate3d("+i+"px, "+s+"px, 0)",transform:"translate3d("+i+"px, "+s+"px, 0)"});break}};e.fn.removeAnimate=function(t,n){var r=n.data("position")||t.position,i=0,s=0;e(this).css({top:"0",opacity:"0","-webkit-transform":"translate3d("+i+", "+s+"px, 0)","-moz-transform":"translate3d("+i+", "+s+"px, 0)","-ms-transform":"translate3d("+i+", "+s+"px, 0)",transform:"translate3d("+i+", "+s+"px, 0)"})};e.fn.label_better=function(n){var r=e.extend({},t,n),i=e(this),s="focus",o="blur";if(r.easing=="bounce")r.easing="cubic-bezier(0.175, 0.885, 0.420, 1.310)";i.each(function(t,n){var i=e(this),u=i.data("position")||r.position;i.wrapAll("<div class='lb_wrap' style='position:relative; display: inline;'></div>");if(i.val().length>0){var a=i.data("new-placeholder")||i.attr("placeholder");e("<div class='lb_label "+u+"'>"+a+"</div>").css("opacity","0").insertAfter(i).animateLabel(r,i)}i.bind(s,function(){if(i.val().length<1){var t=i.data("new-placeholder")||i.attr("placeholder"),n=i.data("position")||r.position;e("<div class='lb_label "+n+"'>"+t+"</div>").css("opacity","0").insertAfter(i).animateLabel(r,i)}if(r.hidePlaceholderOnFocus==true){i.data("default-placeholder",i.attr("placeholder"));i.attr("placeholder","")}i.parent().find(".lb_label").addClass("active")}).bind(o,function(){if(i.val().length<1){i.parent().find(".lb_label").bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd",function(){e(this).remove()}).removeAnimate(r,i)}if(r.hidePlaceholderOnFocus==true){i.attr("placeholder",i.data("default-placeholder"));i.data("default-placeholder","")}i.parent().find(".lb_label").removeClass("active")})})}}(window.jQuery)

