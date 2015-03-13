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
