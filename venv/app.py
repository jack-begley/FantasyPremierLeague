from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
