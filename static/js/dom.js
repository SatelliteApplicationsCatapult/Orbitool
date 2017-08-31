'use strict';
var $ = (function() {
    function dom(selector) {
        if(!(this instanceof dom)) {
            return new dom(selector);
        }
        if (typeof selector === 'string' || selector instanceof String){
            this.elements = Array.from(document.querySelectorAll(selector));
        } else {
            this.elements = Array.of(selector);
        }
    }
    dom.prototype.iterate = function(func) {
        this.elements.forEach(func);
        return this;
    };
    dom.prototype.addClass = function() {
        var klasses = arguments;
        return this.iterate(function(element) {
            element.classList.add.apply(element.classList, klasses);
        });
    };
    dom.prototype.removeClass = function() {
        var klasses = arguments;
        return this.iterate(function(element) {
            element.classList.remove.apply(element.classList, klasses);
        });
    };
    dom.prototype.toggleClass = function() {
        var klasses = arguments;
        return this.iterate(function(element) {
            element.classList.toggle.apply(element.classList, klasses);
        });
    };
    dom.prototype.css = function(name,value) {
        return this.iterate(function(element) {
            element.style[name] = value;
        });
    };
    dom.prototype.height = function(sumAll = false){
        if(sumAll){
            var sum = 0;
            this.iterate(function(obj){
                sum += obj.clientHeight;
            });
            return sum;
        } else {
            return this.elements[0].clientHeight;
        }
    };
    dom.prototype.width = function(sumAll = false){
        if(sumAll){
            var sum = 0;
            this.iterate(function(obj){
                sum += obj.clientWidth;
            });
            return sum;
        } else {
            return this.elements[0].clientWidth;
        }
    };
    dom.prototype.on = function(event,func) {
        return this.iterate(function(element) {
            element.addEventListener(event,func)
        });
    };
    dom.prototype.classSelector = function() {
        return this.elements[0].localName+'.'+this.elements[0].classList.join('.');
    };
    dom.prototype.find = function(selector) {
        var subElements=[];
        this.iterate(function(element) {
            subElements.push.apply(subElements, element.querySelectorAll(selector));
        });
        this.elements=subElements;
        return this;
    };
    dom.prototype.get = function(){
        return this.elements[0];
    };
    dom.extend = function(name, func) {
        this.prototype[name] = func;
    };
    dom.ready = function(func) {
        document.addEventListener("DOMContentLoaded", func);
    };
    return dom;
})();
