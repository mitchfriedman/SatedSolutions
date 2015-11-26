import sys
from app.application import create_app


app = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return response


if __name__ == '__main__':
    debug = True if len(sys.argv) > 1 else False
    app.run(host='0.0.0.0', debug=debug, port=5000, threaded=True)

