from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from generator import get_parsed_reponse

server = Flask(__name__)
CORS(server)

url = ""

@server.route('/')
def home() :
    return render_template('template.html')

@server.route('/loading')
def loading() :
    return

@server.route('/get_url', methods=['POST'])
def handle_json() :
    data = request.get_json()

    global url
    url = data.get('url')

@server.route('/generate_ideas')
def generate_ideas() :
    parsed_reponse = get_parsed_reponse(url)
    return render_template('template1.html', json_packet = jsonify({"message" : parsed_reponse}))
