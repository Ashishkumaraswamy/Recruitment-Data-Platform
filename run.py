from app import app
from app.module.routes import *

if __name__ == '__main__':
    app.run(host='localhost', port=8800, debug=True)
