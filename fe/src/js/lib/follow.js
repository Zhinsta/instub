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

