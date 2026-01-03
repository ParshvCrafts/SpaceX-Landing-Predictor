"""
Flask server for SpaceX Landing Prediction Website
Configured for Render.com deployment
"""

import os
from flask import Flask, send_from_directory, send_file

app = Flask(__name__, static_folder='.', static_url_path='')

# Serve index.html at root
@app.route('/')
def serve_index():
    return send_file('index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return send_file('index.html')  # SPA fallback

# Health check for Render
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
