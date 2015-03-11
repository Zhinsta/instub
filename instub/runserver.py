# coding: utf-8

from gevent import monkey
monkey.patch_all()  # NOQA

from gevent.wsgi import WSGIServer

from instub.app import app


def main():
    # app.run(host='localhost', port=5000, debug=app.config['DEBUG'])
    app.debug = app.config['DEBUG']
    http_server = WSGIServer(('localhost', 6000), app)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
