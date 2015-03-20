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
