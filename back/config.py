from flask import Flask;
import os;

base = os.path.abspath(os.path.dirname(__file__))
front = os.path.join(base, '..', 'front')
templates = os.path.join(front, 'templates')

# app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'front', 'templates'))
app = Flask(__name__, template_folder=templates)