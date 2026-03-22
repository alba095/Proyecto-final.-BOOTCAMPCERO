from flask import Flask
from models.database import init_db, add_mov

app = Flask(__name__)
init_db()

from controllers.routes import *

if __name__ == "__main__":
    app.run(debug=True)