var $ = require('./lib/$');

require('./lib/like')();
require('./lib/follow')();

var triggerByHover = function (trigger, target) {
    trigger = $(trigger);
    target = $(target);
    if ((!trigger.nodeName && !trigger.length) || (!target.nodeName && !target.length)) {
        return;
    }

    var mouseOver = false;
    trigger.on('mouseenter', function () {
        target.style.display = 'block';
        mouseOver = true;
    });

    target.on('mouseenter', function () {
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

    trigger.on('mouseleave', mouseout);
    target.on('mouseleave', mouseout);
};

triggerByHover('#logo', '#navMenu');
triggerByHover('#state', '#stateMenu');


