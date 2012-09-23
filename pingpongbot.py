#!/usr/bin/env python
"""Usage: pongbot.py teamname host port """

import json
import logging
import socket
import argparse

class JsonOverTcp(object):
    """Send and receive newline delimited JSON messages over TCP."""
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, int(port)))

    def send(self, data):
        self._socket.sendall(json.dumps(data) + '\n')

    def receive(self):
        data = ''
        while '\n' not in data:
            data += self._socket.recv(1)
        return json.loads(data)


class PingPongBot(object):
    def __init__(self, connection, log):
        self._connection = connection
        self._log = log

    def open_browser_url(self, url):
        pass

    def run(self, teamname):
        self._connection.send({'msgType': 'join', 'data': teamname})
        self._response_loop()

    def _response_loop(self):
        response_handlers = {
                'joined': self._game_joined,
                'gameStarted': self._game_started,
                'gameIsOn': self._make_move,
                'gameIsOver': self._game_over
                }
        while True:
            response = self._connection.receive()
            msg_type, data = response['msgType'], response['data']
            if msg_type in response_handlers:
                response_handlers[msg_type](data)
            else:
                self._log.error('Unkown response: %s' % msg_type)

    def _game_joined(self, data):
        self._log.info('Game visualization url: %s' % data)
        self.open_browser_url(data)

    def _game_started(self, data):
        self._log.info('Game started: %s vs. %s' % (data[0], data[1]))

    def _make_move(self, data):
        x = sign(data['ball']['pos']['y'] - data['left']['y'])
        self._connection.send({'msgType': 'changeDir', 'data': x})

    def _game_over(self, data):
        self._log.info('Game ended. Winner: %s' % data)

def sign(value):
    return +1.0 if value >= 0.0 else -1.0

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.INFO)
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="run hwo bot")
    parser.add_argument('-w', dest='browser_view_on', action='store_true')
    parser.add_argument('teamname')
    parser.add_argument('hostname')
    parser.add_argument('port')
    args = parser.parse_args()

    bot = PingPongBot(JsonOverTcp(args.hostname, args.port), log)
    if args.browser_view_on:
        import webbrowser
        bot.open_browser_url = webbrowser.open
    bot.run(args.teamname)

#    try:
#        teamname, hostname, port = sys.argv[1:]
#        PingPongBot(JsonOverTcp(hostname, port), log).run(teamname)
#    except TypeError:
#        sys.exit(__doc__)
