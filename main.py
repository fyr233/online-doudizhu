from datetime import timedelta
import doudizhu
from doudizhu import Card
from doudizhu import check_card_type
from doudizhu import cards_greater
import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from random import randint

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=10)

class Room(object):

    def __init__(self, name):
        self.players = []
        self.name = name
        self.cards_pool = doudizhu.new_game()
        self.state = 'waiting'#call, playing
        self.grabchoice = []
        self.outcard_log=[]
        self.publicmessage = ''
        self.firstid = randint(0,2)
    
    def AddPlayer(self, player):
        self.players.append(player)
        self.publicmessage = player.name+'加入房间'
        return len(self.players) - 1

    def FindPlayerbyName(self, playername):
        for i in range(len(players)):
            if players[i].name == playeranme:
                return i
        return -1
    
    def IsFull(self):
        return len(self.players) >= 3

    def IsReady(self):
        isready = True
        for each in self.players:
            isready = isready and (each.state=='ready')
        return isready

    def DistributeCards(self):
        self.publicmessage = '开始发牌'
        self.players[0].card_left = self.cards_pool[0]
        self.players[1].card_left = self.cards_pool[1]
        self.players[2].card_left = self.cards_pool[2]

        self.players[self.firstid].state = 'grabbing on turn'
        self.players[(self.firstid+1)%3].state = 'waiting'
        self.players[(self.firstid+2)%3].state = 'waiting'

    def GrabDiZhu(self, playerid, choice):
        if len(self.grabchoice)==0:
            self.grabchoice.append(choice)
            self.players[self.firstid].state = 'waiting'
            self.players[(self.firstid+1)%3].state = 'grabbing on turn'
        elif len(self.grabchoice)==1:
            self.grabchoice.append(choice)
            self.players[(self.firstid+1)%3].state = 'waiting'
            self.players[(self.firstid+2)%3].state = 'grabbing on turn'
        elif len(self.grabchoice)==2:
            self.grabchoice.append(choice)
            if self.grabchoice in [['1', '0', '0']]:
                self.publicmessage = self.players[self.firstid].name+'成为地主'
                self.players[self.firstid].role = 'dizhu'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'nongmin'
                self.players[self.firstid].state = 'playing'
                self.players[(self.firstid+2)%3].state = 'waiting'
                self.players[self.firstid].card_left.extend(self.cards_pool[3])
            elif self.grabchoice in [['1', '1', '0'], ['0', '1', '0']]:
                self.publicmessage = self.players[(self.firstid+1)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].state = 'playing'
                self.players[(self.firstid+2)%3].state = 'waiting'
                self.players[(self.firstid+1)%3].card_left.extend(self.cards_pool[3])
            elif self.grabchoice in [['0', '1', '1'], ['0', '0', '1']]:
                self.publicmessage = self.players[(self.firstid+2)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].state = 'playing'
                self.players[(self.firstid+2)%3].card_left.extend(self.cards_pool[3])
            elif self.grabchoice==['0', '0', '0']:
                self.publicmessage = '重新开始'
                DistributeCards()
                self.grabchoice=[]
                self.players[self.firstid].state = 'grabbing on turn'
                self.players[(self.firstid+1)%3].state = 'waiting'
                self.players[(self.firstid+2)%3].state = 'waiting'
            else:
                self.players[(self.firstid+2)%3].state = 'waiting'
                self.players[(self.firstid+3)%3].state = 'grabbing on turn'
        elif len(self.grabchoice)==3:
            self.grabchoice.append(choice)
            if self.grabchoice in [['1', '1', '1', '1'], ['1', '0', '1', '1']]:
                self.publicmessage = self.players[self.firstid].name+'成为地主'
                self.players[self.firstid].role = 'dizhu'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'nongmin'
                self.players[self.firstid].state = 'playing'
                self.players[(self.firstid+2)%3].state = 'waiting'
                self.players[(self.firstid+0)%3].card_left.extend(self.cards_pool[3])
            elif self.grabchoice in [['1', '1', '1', '0'], ['1', '0', '1', '0']]:
                self.publicmessage = self.players[(self.firstid+2)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].state = 'playing'
                self.players[(self.firstid+2)%3].card_left.extend(self.cards_pool[3])
    def Play(self, playerid, cards):
        if len(self.outcard_log)>0:
            if self.outcard_log[-1][0]==playerid:
                self.outcard_log.append([playerid, cards])
                for each in cards:
                    for i in range(len(self.players[playerid].card_left)):
                        if self.players[playerid].card_left[i]==each:
                            self.players[playerid].card_left.pop(i)
                            break
                if self.players[playerid].card_left==[]:
                    Win(playerid)
                else:
                    self.players[playerid].state = 'waiting'
                    self.players[(playerid+1)%3].state = 'playing'
            else:
                b, t = cards_greater(cards, outcard_list[-1])
                if b:
                    self.outcard_log.append([playerid, cards])
                    for each in cards:
                        for i in range(len(self.players[playerid].card_left)):
                            if self.players[playerid].card_left[i]==each:
                                self.players[playerid].card_left.pop(i)
                                break
                    if self.players[playerid].card_left==[]:
                        Win(playerid)
                    else:
                        self.players[playerid].state = 'waiting'
                        self.players[(playerid+1)%3].state = 'playing'
                else:
                    self.publicmessage = self.players[(self.firstid+2)%3].name+'，你出的牌有点小'
        else:
            self.outcard_log.append([playerid, cards])
            for each in cards:
                for i in range(len(self.players[playerid].card_left)):
                    if self.players[playerid].card_left[i]==each:
                        self.players[playerid].card_left.pop(i)
                        break
            if self.players[playerid].card_left==[]:
                Win(playerid)
            else:
                self.players[playerid].state = 'waiting'
                self.players[(playerid+1)%3].state = 'playing'
    
    def Pass(self, playerid):
        self.players[playerid].state = 'waiting'
        self.players[(playerid+1)%3].state = 'playing'

    def Win(self, playerid):
        self.publicmessage = self.players[(self.firstid+2)%3].name+'赢了'
        self.players[playerid].state = 'win'
        if self.players[(playerid+1)%3].role==self.players[playerid].role:
            self.players[(playerid+1)%3].state = 'win'
        else:
            self.players[(playerid+1)%3].state = 'loss'
        if self.players[(playerid+2)%3].role==self.players[playerid].role:
            self.players[(playerid+2)%3].state = 'win'
        else:
            self.players[(playerid+2)%3].state = 'loss'
    
    def IsOver(self):
        isover = True
        for each in self.players:
            isover = isover and (each.state=='over')
        return isover


class Player(object):

    def __init__(self, name):
        self.name = name
        self.state = 'notready'
        self.score = 0.0
        self.role = ''
        self.card_left = []

def CreateRoom(name):
    newroom = Room(name)
    room_list.append(newroom)
    return len(room_list) - 1

def DestroyRoom(i):
    room_list.pop(i)

def FindRoombyName(name):
    for i in range(len(room_list)):
        if room_list[i].name == name:
            return i
    return -1


@app.route('/')
def indexpage():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    roomname = request.form['roomname']
    playername = request.form['playername']
    roomid = FindRoombyName(roomname)
    if roomid<0 :#房间不存在，创建新房
        newroomid = CreateRoom(roomname)
        newplayer = Player(playername)
        newplayerid = room_list[newroomid].AddPlayer(newplayer)
        return jsonify({'result':'登录成功',
                        'roomid':str(newroomid),
                        'playerid':str(newplayerid)})
    else:
        playerid = room_list[roomid].FindPlayerbyName(playername)
        if playerid < 0:
            if room_list[roomid].IsFull():
                return jsonify({'error':'房间已满'})
            else:
                newplayer = Player(playername)
                room_list[roomid].AddPlayer(newplayer)
                return jsonify({'result':'登录成功',
                                'roomid':str(newroomid),
                                'playerid':str(newplayerid)})
        else:
            return jsonify({'result':'您已存在',
                            'roomid':str(newroomid),
                            'playerid':str(newplayerid)})

@app.route('/ready', methods=['POST'])
def getready():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    room_list[roomid].FindPlayerbyId(playerid).state = 'ready'

    if room_list[roomid].IsReady():
        room_list[roomid].DistributeCards()

@app.route('/grab', methods=['POST'])
def grab():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    choice = request.form['choice']
    if room_list[roomid].players[playerid].state=='grabbing on turn':
        room_list[roomid].GrabDiZhu(playerid, choice)

@app.route('/out', methods=['POST'])
def outcard():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    cards = Card.card_ints_from_string(request.form['cards'])
    b, t = check_card_type(cards)
    if b :
        if room_list[roomid].players[playerid].state=='playing':
            room_list[roomid].Play(playerid, cards)
    else:
        return jsonify({'error':'牌型不符合要求'})

@app.route('/pass', methods=['POST'])
def skip():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    if room_list[roomid].players[playerid].state=='playing':
        room_list[roomid].Pass(playerid)

@app.route('/quit', methods=['POST'])
def over():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    room_list[roomid].FindPlayerbyId(playerid).state = 'over'

    if room_list[roomid].IsOver():
        DestroyRoom(i)

@app.route('/refresh', methods=['POST'])
def refresh():
    roomid = request.form['roomid']
    playerid = request.form['playerid']
    return jsonify({'roomname':room_list[roomid].name,
                    'playername':room_list[roomid].players[playerid].name,
                    'playerstate':room_list[roomid].players[playerid].state,
                    'playerscore':str(room_list[roomid].players[playerid].score),
                    'playerrole':room_list[roomid].players[playerid].role,
                    'playercards':str(room_list[roomid].players[playerid].card_left)})

room_list = []

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
