(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"./src/js//g.js":[function(require,module,exports){
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



},{"./lib/$":"/Users/gs/github/instub/fe/src/js/lib/$.js","./lib/follow":"/Users/gs/github/instub/fe/src/js/lib/follow.js","./lib/like":"/Users/gs/github/instub/fe/src/js/lib/like.js"}],"/Users/gs/github/instub/fe/src/js/lib/$.js":[function(require,module,exports){
// Node covers all elements, but also the document objects
var node = Node.prototype;
var nodeList = NodeList.prototype;
var forEach = 'forEach';
var trigger = 'trigger';
var each = [][forEach];
// note: createElement requires a string in Firefox
var dummy = document.createElement('i');

nodeList[forEach] = each;

// we have to explicitly add a window.on as it's not included
// in the Node object.
window.on = node.on = function (event, fn) {
    this.addEventListener(event, fn, false);

    // allow for chaining
    return this;
};

nodeList.on = function (event, fn) {
    this[forEach](function (el) {
      el.on(event, fn);
    });
    return this;
};

// we save a few bytes (but none really in compression)
// by using [trigger] - really it's for consistency in the
// source code.
window[trigger] = node[trigger] = function (type, data) {
    // construct an HTML event. This could have
    // been a real custom event
    var event = document.createEvent('HTMLEvents');
    event.initEvent(type, true, true);
    event.data = data || {};
    event.eventName = type;
    event.target = this;
    this.dispatchEvent(event);
    return this;
};

nodeList[trigger] = function (event) {
    this[forEach](function (el) {
        el[trigger](event);
    });
    return this;
};

$ = function (s) {
    // querySelectorAll requires a string with a length
    // otherwise it throws an exception
    var r = document.querySelectorAll(s || '☺');
    var length = r.length;
    // if we have a single element, just return that.
    // if there's no matched elements, return a nodeList to chain from
    // else return the NodeList collection from qSA
    return length == 1 ? r[0] : r;
};

// $.on and $.trigger allow for pub/sub type global
// custom events.
$.on = node.on.bind(dummy);
$[trigger] = node[trigger].bind(dummy);


module.exports = $;


},{}],"/Users/gs/github/instub/fe/src/js/lib/api.js":[function(require,module,exports){
var request = require('./request');
var api = {
    like: function(mid, success) {
        request.get(
            '/apis/like/',
            {mid: mid, action: 'like'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            }
        );
    },
    unlike: function(mid, success) {
        request.get(
            '/apis/like/',
            {mid: mid, action: 'unlike'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            }
        );
    },
    islike: function(mid, success) {
        request.get(
            '/apis/islike/',
            {mid: mid},
            function(data) {
                if (success) {
                    success(data.result);
                }
            }
        );
    },
    follow: function(ukey, success) {
        request.get(
            '/apis/follow/',
            {ukey: ukey, action: 'follow'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            }
        );
    },
    unfollow: function(ukey, success) {
        request.get(
            '/apis/follow/',
            {ukey: ukey, action: 'unfollow'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            }
        );
    }
};


module.exports = api;

},{"./request":"/Users/gs/github/instub/fe/src/js/lib/request.js"}],"/Users/gs/github/instub/fe/src/js/lib/follow.js":[function(require,module,exports){
var request = require('./request');
var $ = require('./$');
var api = require('./api');

module.exports = function () {
    $('.jsFollow').on('click', function (e) {
        e.preventDefault();
        var dataset = this.dataset;
        var action = dataset.action;
        var ukey = dataset.ukey;

        api[action](ukey, function () {
            var newAction = action === 'follow' ? 'unfollow' : 'follow';
            dataset.action = newAction;
            this.innerHTML = newAction;
        });
    });
};


},{"./$":"/Users/gs/github/instub/fe/src/js/lib/$.js","./api":"/Users/gs/github/instub/fe/src/js/lib/api.js","./request":"/Users/gs/github/instub/fe/src/js/lib/request.js"}],"/Users/gs/github/instub/fe/src/js/lib/like.js":[function(require,module,exports){
var request = require('./request');
var $ = require('./$');
var api = require('./api');

module.exports = function () {
    $('.jsLove').on('click', function (e) {
        e.preventDefault();
        var dataset = this.dataset;
        var action = dataset.action;
        var mid = dataset.mid;

        api[action](mid, function () {
            dataset.action = (action === 'like') ? 'unlike' : 'like';
        });
    });
};

},{"./$":"/Users/gs/github/instub/fe/src/js/lib/$.js","./api":"/Users/gs/github/instub/fe/src/js/lib/api.js","./request":"/Users/gs/github/instub/fe/src/js/lib/request.js"}],"/Users/gs/github/instub/fe/src/js/lib/request.js":[function(require,module,exports){
function request(type, url, opts, callback) {
    var xhr = new XMLHttpRequest();
    var pd;

    if (typeof opts === 'function') {
        callback = opts;
        opts = null;
    }

    xhr.open(type, url);

    if (type === 'POST' && opts) {
        pd = JSON.stringify(opts);

        xhr.setRequestHeader('Content-Type', 'application/json');
    }

    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function () {
        callback.call(xhr, null, JSON.parse(xhr.response));
    };
    xhr.onerror = function () {
        callback.call(xhr, true);
    };

    xhr.send(opts ? pd : null);
    return xhr;
}

module.exports = {
    get: request.bind(this, 'GET'),
    post: request.bind(this, 'POST')
};


},{}]},{},["./src/js//g.js"])
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCIuL3NyYy9qcy8vZy5qcyIsIi9Vc2Vycy9ncy9naXRodWIvaW5zdHViL2ZlL3NyYy9qcy9saWIvJC5qcyIsIi9Vc2Vycy9ncy9naXRodWIvaW5zdHViL2ZlL3NyYy9qcy9saWIvYXBpLmpzIiwiL1VzZXJzL2dzL2dpdGh1Yi9pbnN0dWIvZmUvc3JjL2pzL2xpYi9mb2xsb3cuanMiLCIvVXNlcnMvZ3MvZ2l0aHViL2luc3R1Yi9mZS9zcmMvanMvbGliL2xpa2UuanMiLCIvVXNlcnMvZ3MvZ2l0aHViL2luc3R1Yi9mZS9zcmMvanMvbGliL3JlcXVlc3QuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUN2Q0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3BFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQzdEQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ25CQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ2hCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gZSh0LG4scil7ZnVuY3Rpb24gcyhvLHUpe2lmKCFuW29dKXtpZighdFtvXSl7dmFyIGE9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtpZighdSYmYSlyZXR1cm4gYShvLCEwKTtpZihpKXJldHVybiBpKG8sITApO3ZhciBmPW5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIrbytcIidcIik7dGhyb3cgZi5jb2RlPVwiTU9EVUxFX05PVF9GT1VORFwiLGZ9dmFyIGw9bltvXT17ZXhwb3J0czp7fX07dFtvXVswXS5jYWxsKGwuZXhwb3J0cyxmdW5jdGlvbihlKXt2YXIgbj10W29dWzFdW2VdO3JldHVybiBzKG4/bjplKX0sbCxsLmV4cG9ydHMsZSx0LG4scil9cmV0dXJuIG5bb10uZXhwb3J0c312YXIgaT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2Zvcih2YXIgbz0wO288ci5sZW5ndGg7bysrKXMocltvXSk7cmV0dXJuIHN9KSIsInZhciAkID0gcmVxdWlyZSgnLi9saWIvJCcpO1xuXG5yZXF1aXJlKCcuL2xpYi9saWtlJykoKTtcbnJlcXVpcmUoJy4vbGliL2ZvbGxvdycpKCk7XG5cbnZhciB0cmlnZ2VyQnlIb3ZlciA9IGZ1bmN0aW9uICh0cmlnZ2VyLCB0YXJnZXQpIHtcbiAgICB0cmlnZ2VyID0gJCh0cmlnZ2VyKTtcbiAgICB0YXJnZXQgPSAkKHRhcmdldCk7XG4gICAgaWYgKCghdHJpZ2dlci5ub2RlTmFtZSAmJiAhdHJpZ2dlci5sZW5ndGgpIHx8ICghdGFyZ2V0Lm5vZGVOYW1lICYmICF0YXJnZXQubGVuZ3RoKSkge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdmFyIG1vdXNlT3ZlciA9IGZhbHNlO1xuICAgIHRyaWdnZXIub24oJ21vdXNlZW50ZXInLCBmdW5jdGlvbiAoKSB7XG4gICAgICAgIHRhcmdldC5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJztcbiAgICAgICAgbW91c2VPdmVyID0gdHJ1ZTtcbiAgICB9KTtcblxuICAgIHRhcmdldC5vbignbW91c2VlbnRlcicsIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgbW91c2VPdmVyID0gdHJ1ZTtcbiAgICB9KTtcblxuICAgIHZhciBtb3VzZW91dCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgbW91c2VPdmVyID0gZmFsc2U7XG4gICAgICAgIHNldFRpbWVvdXQoZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgaWYgKCFtb3VzZU92ZXIpIHtcbiAgICAgICAgICAgICAgICB0YXJnZXQuc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSwgMjUwKTtcbiAgICB9O1xuXG4gICAgdHJpZ2dlci5vbignbW91c2VsZWF2ZScsIG1vdXNlb3V0KTtcbiAgICB0YXJnZXQub24oJ21vdXNlbGVhdmUnLCBtb3VzZW91dCk7XG59O1xuXG50cmlnZ2VyQnlIb3ZlcignI2xvZ28nLCAnI25hdk1lbnUnKTtcbnRyaWdnZXJCeUhvdmVyKCcjc3RhdGUnLCAnI3N0YXRlTWVudScpO1xuXG5cbiIsIi8vIE5vZGUgY292ZXJzIGFsbCBlbGVtZW50cywgYnV0IGFsc28gdGhlIGRvY3VtZW50IG9iamVjdHNcbnZhciBub2RlID0gTm9kZS5wcm90b3R5cGU7XG52YXIgbm9kZUxpc3QgPSBOb2RlTGlzdC5wcm90b3R5cGU7XG52YXIgZm9yRWFjaCA9ICdmb3JFYWNoJztcbnZhciB0cmlnZ2VyID0gJ3RyaWdnZXInO1xudmFyIGVhY2ggPSBbXVtmb3JFYWNoXTtcbi8vIG5vdGU6IGNyZWF0ZUVsZW1lbnQgcmVxdWlyZXMgYSBzdHJpbmcgaW4gRmlyZWZveFxudmFyIGR1bW15ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaScpO1xuXG5ub2RlTGlzdFtmb3JFYWNoXSA9IGVhY2g7XG5cbi8vIHdlIGhhdmUgdG8gZXhwbGljaXRseSBhZGQgYSB3aW5kb3cub24gYXMgaXQncyBub3QgaW5jbHVkZWRcbi8vIGluIHRoZSBOb2RlIG9iamVjdC5cbndpbmRvdy5vbiA9IG5vZGUub24gPSBmdW5jdGlvbiAoZXZlbnQsIGZuKSB7XG4gICAgdGhpcy5hZGRFdmVudExpc3RlbmVyKGV2ZW50LCBmbiwgZmFsc2UpO1xuXG4gICAgLy8gYWxsb3cgZm9yIGNoYWluaW5nXG4gICAgcmV0dXJuIHRoaXM7XG59O1xuXG5ub2RlTGlzdC5vbiA9IGZ1bmN0aW9uIChldmVudCwgZm4pIHtcbiAgICB0aGlzW2ZvckVhY2hdKGZ1bmN0aW9uIChlbCkge1xuICAgICAgZWwub24oZXZlbnQsIGZuKTtcbiAgICB9KTtcbiAgICByZXR1cm4gdGhpcztcbn07XG5cbi8vIHdlIHNhdmUgYSBmZXcgYnl0ZXMgKGJ1dCBub25lIHJlYWxseSBpbiBjb21wcmVzc2lvbilcbi8vIGJ5IHVzaW5nIFt0cmlnZ2VyXSAtIHJlYWxseSBpdCdzIGZvciBjb25zaXN0ZW5jeSBpbiB0aGVcbi8vIHNvdXJjZSBjb2RlLlxud2luZG93W3RyaWdnZXJdID0gbm9kZVt0cmlnZ2VyXSA9IGZ1bmN0aW9uICh0eXBlLCBkYXRhKSB7XG4gICAgLy8gY29uc3RydWN0IGFuIEhUTUwgZXZlbnQuIFRoaXMgY291bGQgaGF2ZVxuICAgIC8vIGJlZW4gYSByZWFsIGN1c3RvbSBldmVudFxuICAgIHZhciBldmVudCA9IGRvY3VtZW50LmNyZWF0ZUV2ZW50KCdIVE1MRXZlbnRzJyk7XG4gICAgZXZlbnQuaW5pdEV2ZW50KHR5cGUsIHRydWUsIHRydWUpO1xuICAgIGV2ZW50LmRhdGEgPSBkYXRhIHx8IHt9O1xuICAgIGV2ZW50LmV2ZW50TmFtZSA9IHR5cGU7XG4gICAgZXZlbnQudGFyZ2V0ID0gdGhpcztcbiAgICB0aGlzLmRpc3BhdGNoRXZlbnQoZXZlbnQpO1xuICAgIHJldHVybiB0aGlzO1xufTtcblxubm9kZUxpc3RbdHJpZ2dlcl0gPSBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICB0aGlzW2ZvckVhY2hdKGZ1bmN0aW9uIChlbCkge1xuICAgICAgICBlbFt0cmlnZ2VyXShldmVudCk7XG4gICAgfSk7XG4gICAgcmV0dXJuIHRoaXM7XG59O1xuXG4kID0gZnVuY3Rpb24gKHMpIHtcbiAgICAvLyBxdWVyeVNlbGVjdG9yQWxsIHJlcXVpcmVzIGEgc3RyaW5nIHdpdGggYSBsZW5ndGhcbiAgICAvLyBvdGhlcndpc2UgaXQgdGhyb3dzIGFuIGV4Y2VwdGlvblxuICAgIHZhciByID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChzIHx8ICfimLonKTtcbiAgICB2YXIgbGVuZ3RoID0gci5sZW5ndGg7XG4gICAgLy8gaWYgd2UgaGF2ZSBhIHNpbmdsZSBlbGVtZW50LCBqdXN0IHJldHVybiB0aGF0LlxuICAgIC8vIGlmIHRoZXJlJ3Mgbm8gbWF0Y2hlZCBlbGVtZW50cywgcmV0dXJuIGEgbm9kZUxpc3QgdG8gY2hhaW4gZnJvbVxuICAgIC8vIGVsc2UgcmV0dXJuIHRoZSBOb2RlTGlzdCBjb2xsZWN0aW9uIGZyb20gcVNBXG4gICAgcmV0dXJuIGxlbmd0aCA9PSAxID8gclswXSA6IHI7XG59O1xuXG4vLyAkLm9uIGFuZCAkLnRyaWdnZXIgYWxsb3cgZm9yIHB1Yi9zdWIgdHlwZSBnbG9iYWxcbi8vIGN1c3RvbSBldmVudHMuXG4kLm9uID0gbm9kZS5vbi5iaW5kKGR1bW15KTtcbiRbdHJpZ2dlcl0gPSBub2RlW3RyaWdnZXJdLmJpbmQoZHVtbXkpO1xuXG5cbm1vZHVsZS5leHBvcnRzID0gJDtcblxuIiwidmFyIHJlcXVlc3QgPSByZXF1aXJlKCcuL3JlcXVlc3QnKTtcbnZhciBhcGkgPSB7XG4gICAgbGlrZTogZnVuY3Rpb24obWlkLCBzdWNjZXNzKSB7XG4gICAgICAgIHJlcXVlc3QuZ2V0KFxuICAgICAgICAgICAgJy9hcGlzL2xpa2UvJyxcbiAgICAgICAgICAgIHttaWQ6IG1pZCwgYWN0aW9uOiAnbGlrZSd9LFxuICAgICAgICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlc3VsdCA9PT0gJ29rJyAmJiBzdWNjZXNzKSB7XG4gICAgICAgICAgICAgICAgICAgIHN1Y2Nlc3MoKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICk7XG4gICAgfSxcbiAgICB1bmxpa2U6IGZ1bmN0aW9uKG1pZCwgc3VjY2Vzcykge1xuICAgICAgICByZXF1ZXN0LmdldChcbiAgICAgICAgICAgICcvYXBpcy9saWtlLycsXG4gICAgICAgICAgICB7bWlkOiBtaWQsIGFjdGlvbjogJ3VubGlrZSd9LFxuICAgICAgICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlc3VsdCA9PT0gJ29rJyAmJiBzdWNjZXNzKSB7XG4gICAgICAgICAgICAgICAgICAgIHN1Y2Nlc3MoKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICk7XG4gICAgfSxcbiAgICBpc2xpa2U6IGZ1bmN0aW9uKG1pZCwgc3VjY2Vzcykge1xuICAgICAgICByZXF1ZXN0LmdldChcbiAgICAgICAgICAgICcvYXBpcy9pc2xpa2UvJyxcbiAgICAgICAgICAgIHttaWQ6IG1pZH0sXG4gICAgICAgICAgICBmdW5jdGlvbihkYXRhKSB7XG4gICAgICAgICAgICAgICAgaWYgKHN1Y2Nlc3MpIHtcbiAgICAgICAgICAgICAgICAgICAgc3VjY2VzcyhkYXRhLnJlc3VsdCk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICApO1xuICAgIH0sXG4gICAgZm9sbG93OiBmdW5jdGlvbih1a2V5LCBzdWNjZXNzKSB7XG4gICAgICAgIHJlcXVlc3QuZ2V0KFxuICAgICAgICAgICAgJy9hcGlzL2ZvbGxvdy8nLFxuICAgICAgICAgICAge3VrZXk6IHVrZXksIGFjdGlvbjogJ2ZvbGxvdyd9LFxuICAgICAgICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlc3VsdCA9PT0gJ29rJyAmJiBzdWNjZXNzKSB7XG4gICAgICAgICAgICAgICAgICAgIHN1Y2Nlc3MoKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICk7XG4gICAgfSxcbiAgICB1bmZvbGxvdzogZnVuY3Rpb24odWtleSwgc3VjY2Vzcykge1xuICAgICAgICByZXF1ZXN0LmdldChcbiAgICAgICAgICAgICcvYXBpcy9mb2xsb3cvJyxcbiAgICAgICAgICAgIHt1a2V5OiB1a2V5LCBhY3Rpb246ICd1bmZvbGxvdyd9LFxuICAgICAgICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlc3VsdCA9PT0gJ29rJyAmJiBzdWNjZXNzKSB7XG4gICAgICAgICAgICAgICAgICAgIHN1Y2Nlc3MoKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICk7XG4gICAgfVxufTtcblxuXG5tb2R1bGUuZXhwb3J0cyA9IGFwaTtcbiIsInZhciByZXF1ZXN0ID0gcmVxdWlyZSgnLi9yZXF1ZXN0Jyk7XG52YXIgJCA9IHJlcXVpcmUoJy4vJCcpO1xudmFyIGFwaSA9IHJlcXVpcmUoJy4vYXBpJyk7XG5cbm1vZHVsZS5leHBvcnRzID0gZnVuY3Rpb24gKCkge1xuICAgICQoJy5qc0ZvbGxvdycpLm9uKCdjbGljaycsIGZ1bmN0aW9uIChlKSB7XG4gICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgdmFyIGRhdGFzZXQgPSB0aGlzLmRhdGFzZXQ7XG4gICAgICAgIHZhciBhY3Rpb24gPSBkYXRhc2V0LmFjdGlvbjtcbiAgICAgICAgdmFyIHVrZXkgPSBkYXRhc2V0LnVrZXk7XG5cbiAgICAgICAgYXBpW2FjdGlvbl0odWtleSwgZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgdmFyIG5ld0FjdGlvbiA9IGFjdGlvbiA9PT0gJ2ZvbGxvdycgPyAndW5mb2xsb3cnIDogJ2ZvbGxvdyc7XG4gICAgICAgICAgICBkYXRhc2V0LmFjdGlvbiA9IG5ld0FjdGlvbjtcbiAgICAgICAgICAgIHRoaXMuaW5uZXJIVE1MID0gbmV3QWN0aW9uO1xuICAgICAgICB9KTtcbiAgICB9KTtcbn07XG5cbiIsInZhciByZXF1ZXN0ID0gcmVxdWlyZSgnLi9yZXF1ZXN0Jyk7XG52YXIgJCA9IHJlcXVpcmUoJy4vJCcpO1xudmFyIGFwaSA9IHJlcXVpcmUoJy4vYXBpJyk7XG5cbm1vZHVsZS5leHBvcnRzID0gZnVuY3Rpb24gKCkge1xuICAgICQoJy5qc0xvdmUnKS5vbignY2xpY2snLCBmdW5jdGlvbiAoZSkge1xuICAgICAgICBlLnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgIHZhciBkYXRhc2V0ID0gdGhpcy5kYXRhc2V0O1xuICAgICAgICB2YXIgYWN0aW9uID0gZGF0YXNldC5hY3Rpb247XG4gICAgICAgIHZhciBtaWQgPSBkYXRhc2V0Lm1pZDtcblxuICAgICAgICBhcGlbYWN0aW9uXShtaWQsIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIGRhdGFzZXQuYWN0aW9uID0gKGFjdGlvbiA9PT0gJ2xpa2UnKSA/ICd1bmxpa2UnIDogJ2xpa2UnO1xuICAgICAgICB9KTtcbiAgICB9KTtcbn07XG4iLCJmdW5jdGlvbiByZXF1ZXN0KHR5cGUsIHVybCwgb3B0cywgY2FsbGJhY2spIHtcbiAgICB2YXIgeGhyID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7XG4gICAgdmFyIHBkO1xuXG4gICAgaWYgKHR5cGVvZiBvcHRzID09PSAnZnVuY3Rpb24nKSB7XG4gICAgICAgIGNhbGxiYWNrID0gb3B0cztcbiAgICAgICAgb3B0cyA9IG51bGw7XG4gICAgfVxuXG4gICAgeGhyLm9wZW4odHlwZSwgdXJsKTtcblxuICAgIGlmICh0eXBlID09PSAnUE9TVCcgJiYgb3B0cykge1xuICAgICAgICBwZCA9IEpTT04uc3RyaW5naWZ5KG9wdHMpO1xuXG4gICAgICAgIHhoci5zZXRSZXF1ZXN0SGVhZGVyKCdDb250ZW50LVR5cGUnLCAnYXBwbGljYXRpb24vanNvbicpO1xuICAgIH1cblxuICAgIHhoci5zZXRSZXF1ZXN0SGVhZGVyKCdYLVJlcXVlc3RlZC1XaXRoJywgJ1hNTEh0dHBSZXF1ZXN0Jyk7XG4gICAgeGhyLm9ubG9hZCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgY2FsbGJhY2suY2FsbCh4aHIsIG51bGwsIEpTT04ucGFyc2UoeGhyLnJlc3BvbnNlKSk7XG4gICAgfTtcbiAgICB4aHIub25lcnJvciA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgY2FsbGJhY2suY2FsbCh4aHIsIHRydWUpO1xuICAgIH07XG5cbiAgICB4aHIuc2VuZChvcHRzID8gcGQgOiBudWxsKTtcbiAgICByZXR1cm4geGhyO1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHtcbiAgICBnZXQ6IHJlcXVlc3QuYmluZCh0aGlzLCAnR0VUJyksXG4gICAgcG9zdDogcmVxdWVzdC5iaW5kKHRoaXMsICdQT1NUJylcbn07XG5cbiJdfQ==
