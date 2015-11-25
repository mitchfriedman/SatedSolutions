import sys
from app.application import create_app

app = create_app()

if __name__ == '__main__':
    debug = True if len(sys.argv) > 1 else False
    app.run(host='0.0.0.0', debug=debug, port=5000)
