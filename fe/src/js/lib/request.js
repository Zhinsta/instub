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

