import sys
sys.path.insert(0, 'C:/Users/JackBegley/source/repos/FantasyPremierLeague')
from flask import Flask, jsonify, request
from gameweekSummary import playerInfoBySurnameJSON

app = Flask(__name__)

@app.route('/playerinfo', methods=['GET'])
def get_player_info():
    try:
        playerSurname = request.args.get('surname')
        print("Surname: ", playerSurname)
        player_info = playerInfoBySurnameJSON(playerSurname)
        return jsonify(player_info)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)