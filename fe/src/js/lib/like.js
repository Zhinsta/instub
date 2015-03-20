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
