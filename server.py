from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

@server.route('/')
def home() :
    return render_template('template.html')

@server.route('/loading')
def loading() :
    return

@server.route('/ideas')
def ideas() :
    return
