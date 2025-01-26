from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import os
import random
import time
from generator import get_parsed_reponse

server = Flask(__name__)
CORS(server)

# Dictionary to store processed results
processing_results = {}

@server.route('/')
def home():
    return render_template('templates/home.html')

@server.route('/loading')
def loading():
    # The loading page will just show a message and keep polling for the result
    return render_template('loading.html')

@server.route('/result/<request_id>')
def result(request_id):
    # Retrieve the processed result for the specific request_id
    result = processing_results.get(request_id)
    if result:
        # Pass the result to the template
        return render_template('result.html', result=result)
    else:
        # If no result found, redirect back to home
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
            # Simulate processing (e.g., waiting for `get_parsed_reponse`)
            parsed_response = get_parsed_reponse(url)
            print(parsed_response)
            # Store the response in the dictionary
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
    # Check if the result is ready for the given request_id
    result = processing_results.get(request_id)
    if result:
        return jsonify({"message": "Result available"}), 200
    else:
        return jsonify({"message": "Still processing..."}), 202

if __name__ == "__main__":
    server.run(debug=True, host='0.0.0.0', port=5000)