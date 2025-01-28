from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS support
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def encode(key, message):
    try:
        enc = []
        for i in range(len(message)):
            key_c = key[i % len(key)]
            enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()
    except Exception as e:
        print(f"Encoding error: {str(e)}")
        return None

def decode(key, message):
    try:
        dec = []
        message = base64.urlsafe_b64decode(message).decode()
        for i in range(len(message)):
            key_c = key[i % len(key)]
            dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
        return "".join(dec)
    except Exception as e:
        print(f"Decoding error: {str(e)}")
        return None

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        print(f"Received data: {data}")  # Debug print
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        message = data.get('message')
        key = data.get('key')
        mode = data.get('mode')
        
        if not all([message, key, mode]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if mode == 'e':
            result = encode(key, message)
        elif mode == 'd':
            result = decode(key, message)
        else:
            return jsonify({'error': 'Invalid mode'}), 400
            
        if result is None:
            return jsonify({'error': 'Processing failed'}), 400
            
        return jsonify({'result': result})
        
    except Exception as e:
        print(f"Server error: {str(e)}")  # Debug print
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Server is running'})

if __name__ == '__main__':
    app.run(debug=True)