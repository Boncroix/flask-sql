import os
from flask import Flask

RUTA = os.path.join('balance', 'data', 'balance.db')

app = Flask(__name__)
