from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from generator import get_parsed_reponse

server = Flask(__name__)
CORS(server)

url = ""

@server.route('/')
def home():
    return render_template('home.html')

@server.route('/loading')
def loading():
    return render_template('loading.html')

@server.route('/get_url', methods=['POST'])
def handle_json():
    global url
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Print the full data to check if it's being received correctly
        print("Received data:", data)

        url = data.get('url')  # Extract URL
        print("Received URL:", url)  # Print the extracted URL

        print(get_parsed_reponse(url))

        if url:
            return jsonify({"message": "URL received successfully!"}), 200
        else:
            return jsonify({"message": "No URL provided!"}), 400
    except Exception as e:
        print("Error handling request:", e)
        return jsonify({"message": "Error processing request!"}), 500

@server.route('/generate_ideas')
def generate_ideas():
    # Ensure the URL is set before proceeding
    if not url:
        return jsonify({"message": "No URL set!"}), 400

    parsed_reponse = get_parsed_reponse(url)
    return render_template('home.html', json_packet={"message": parsed_reponse})

if __name__ == "__main__":
    server.run(debug=True, host='0.0.0.0', port=5000)
