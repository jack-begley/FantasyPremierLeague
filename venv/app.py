import sys
sys.path.insert(0, 'C:/Users/JackBegley/source/repos/FantasyPremierLeague')
from flask import Flask, jsonify, request
from gameweekSummary import playerInfoBySurname
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/playerinfo', methods=['GET'])
def get_player_info():
    playerSurname = request.args.get('surname')
    player_info = playerInfoBySurname(playerSurname)
    return jsonify(player_info)


@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)