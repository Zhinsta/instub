# coding: utf-8

from instub.app import app


def main():
    app.run(host='localhost', port=5010, debug=app.config['DEBUG'])

if __name__ == '__main__':
    main()
