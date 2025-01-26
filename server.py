from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import random
from generator import get_parsed_reponse  # Assuming this function returns the parsed response

server = Flask(__name__)
CORS(server)

# Dictionary to store processed results
processing_results = {}

@server.route('/')
def home():
    return render_template('home.html')

@server.route('/loading')
def loading():
    return render_template('loading.html')

@server.route('/result/<request_id>')
def result(request_id):
    # Retrieve the processed result for the specific request_id
    result = processing_results.get(request_id)
    if result:
        # Pass the result as JSON to the result.html template
        return render_template('result.html', result=result)
    else:
        return redirect(url_for('home'))

@server.route('/get_url', methods=['POST'])
def handle_json():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"message": "No URL provided!"}), 400

        # Generate a unique request ID
        request_id = str(random.randint(1000, 9999))  # Simple unique ID

        # Start processing the URL in a separate thread
        def process_url():
            parsed_response = get_parsed_reponse(url)  # Assuming this returns the parsed data
            processing_results[request_id] = parsed_response

        # Start the URL processing in a background thread
        from threading import Thread
        thread = Thread(target=process_url)
        thread.start()

        # Return the request_id to the client to poll for the result
        return jsonify({"message": "URL received successfully!", "request_id": request_id}), 200
    except Exception as e:
        print("Error handling request:", e)
        return jsonify({"message": "Error processing request!"}), 500

@server.route('/get_processed_result/<request_id>', methods=['GET'])
def get_processed_result(request_id):
    # Retrieve the processed result for the specific request_id
    result = processing_results.get(request_id)
    if result:
        return jsonify({"message": "Result available", "result": result}), 200
    else:
        return jsonify({"message": "Still processing..."}), 202

app = server

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
