from flask_frozen import Freezer
from run import app

freezer_app = Freezer(app)

if __name__ == '__main__':
    freezer_app.freeze()