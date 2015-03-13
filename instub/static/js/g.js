(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"./src/js//g.js":[function(require,module,exports){
(function () {

var g = function (id) {
    return document.getElementById(id);
};
var triggerByHover = function (trigger, target) {
    trigger = g(trigger);
    target = g(target);
    var mouseOver = false;
    trigger.addEventListener('mouseenter', function () {
        target.style.display = 'block';
        mouseOver = true;
    });

    target.addEventListener('mouseenter', function () {
        mouseOver = true;
    });

    var mouseout = function () {
        mouseOver = false;
        setTimeout(function () {
            if (!mouseOver) {
                target.style.display = 'none';
            }
        }, 250);
    };

    trigger.addEventListener('mouseleave', mouseout);
    target.addEventListener('mouseleave', mouseout);
};

triggerByHover('logo', 'navMenu');
triggerByHover('state', 'stateMenu');

})();

},{}]},{},["./src/js//g.js"])
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvanMvZy5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCIoZnVuY3Rpb24gKCkge1xuXG52YXIgZyA9IGZ1bmN0aW9uIChpZCkge1xuICAgIHJldHVybiBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChpZCk7XG59O1xudmFyIHRyaWdnZXJCeUhvdmVyID0gZnVuY3Rpb24gKHRyaWdnZXIsIHRhcmdldCkge1xuICAgIHRyaWdnZXIgPSBnKHRyaWdnZXIpO1xuICAgIHRhcmdldCA9IGcodGFyZ2V0KTtcbiAgICB2YXIgbW91c2VPdmVyID0gZmFsc2U7XG4gICAgdHJpZ2dlci5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWVudGVyJywgZnVuY3Rpb24gKCkge1xuICAgICAgICB0YXJnZXQuc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgICAgIG1vdXNlT3ZlciA9IHRydWU7XG4gICAgfSk7XG5cbiAgICB0YXJnZXQuYWRkRXZlbnRMaXN0ZW5lcignbW91c2VlbnRlcicsIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgbW91c2VPdmVyID0gdHJ1ZTtcbiAgICB9KTtcblxuICAgIHZhciBtb3VzZW91dCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgbW91c2VPdmVyID0gZmFsc2U7XG4gICAgICAgIHNldFRpbWVvdXQoZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgaWYgKCFtb3VzZU92ZXIpIHtcbiAgICAgICAgICAgICAgICB0YXJnZXQuc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSwgMjUwKTtcbiAgICB9O1xuXG4gICAgdHJpZ2dlci5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWxlYXZlJywgbW91c2VvdXQpO1xuICAgIHRhcmdldC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWxlYXZlJywgbW91c2VvdXQpO1xufTtcblxudHJpZ2dlckJ5SG92ZXIoJ2xvZ28nLCAnbmF2TWVudScpO1xudHJpZ2dlckJ5SG92ZXIoJ3N0YXRlJywgJ3N0YXRlTWVudScpO1xuXG59KSgpO1xuIl19
