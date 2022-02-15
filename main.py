import socketio
from time import sleep

received = None
status = ''

class SocketRunner:
    socket = socketio.Client()
    lobby = ''

    @staticmethod
    @socket.event
    def connect():
        print('connection established')

    @staticmethod
    @socket.event
    def disconnect():
        print('disconnected from server')

    @staticmethod
    @socket.on('lobby')
    def lobbyUpdate(data):
        global received
        print('lobby updated with', data)
        received = data

    @staticmethod
    @socket.on('game')
    def lobbyUpdate(data):
        global received
        print('game updated with', data)
        received = data

    @staticmethod
    @socket.on('events')
    def lobbyUpdate(data):
        global status
        status = data['message']
        print('event', status)

    def __init__(self, environment, players):
        self.socket.connect(
            'https://pocket-party.herokuapp.com/' if environment == 'p' else 'http://localhost:5000'
        )
        self.players = players
        self.start()
        self.startGame()
        self.readyUp()

    def start(self):
        global received
        self.socket.emit('create-game', {
            'user_id': '1',
            'username': 'python1'
        })
        while received is None:
            sleep(.5)
            continue
        self.lobby = received['lobby_id']
        for i in range(1, self.players):
            self.socket.emit('join-game', {
                'user_id': f'{i + 1}',
                'username': f'python{i + 1}',
                'lobby_id': self.lobby
            })
        sleep(1)

    def startGame(self):
        self.socket.emit('start-game', {
            'lobby_id': self.lobby,
        })
        sleep(1)

    def readyUp(self):
        global status
        while status != 'game-ready':
            sleep(1)
        for i in range(0, self.players):
            self.socket.emit('ready-up', {
                'user_id': f'{i}',
                'lobby_id': self.lobby
            })



if __name__ == '__main__':
    print('Environment options \np: Production, l: Local')
    environment = input('Environment: ')
    # players = int(input('Enter the number of players: '))


    runner = SocketRunner(environment, 4)