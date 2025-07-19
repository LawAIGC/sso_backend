import os

from waitress import serve

from app import app


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 't')
    if debug:
        app.run(host="0.0.0.0", port=9001, debug=True)
    else:
        serve(app, host="0.0.0.0", port=9001)
