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
        for i in range(len(self.players)):
            if self.players[i].name == playername:
                return i
        return -1
    
    def IsFull(self):
        return len(self.players) >= 3

    def IsReady(self, playerid):
        self.publicmessage = self.players[playerid].name+'准备好了'
        if len(self.players)<3:
            return False
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
        if choice=='1':
            self.publicmessage = self.players[playerid].name+'抢了'
        else:
            self.publicmessage = self.players[playerid].name+'8抢'
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
                #self.players[self.firstid].card_left.sort()
            elif self.grabchoice in [['1', '1', '0'], ['0', '1', '0']]:
                self.publicmessage = self.players[(self.firstid+1)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].state = 'playing'
                self.players[(self.firstid+2)%3].state = 'waiting'
                self.players[(self.firstid+1)%3].card_left.extend(self.cards_pool[3])
                #self.players[(self.firstid+1)%3].card_left.sort()
            elif self.grabchoice in [['0', '1', '1'], ['0', '0', '1']]:
                self.publicmessage = self.players[(self.firstid+2)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].state = 'playing'
                self.players[(self.firstid+2)%3].card_left.extend(self.cards_pool[3])
                #self.players[(self.firstid+2)%3].card_left.sort()
            elif self.grabchoice==['0', '0', '0']:
                self.publicmessage = '重新开始'
                self.cards_pool = doudizhu.new_game()
                self.DistributeCards()
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
                #self.players[(self.firstid+0)%3].card_left.sort()
            elif self.grabchoice in [['1', '1', '1', '0'], ['1', '0', '1', '0']]:
                self.publicmessage = self.players[(self.firstid+2)%3].name+'成为地主'
                self.players[(self.firstid+0)%3].role = 'nongmin'
                self.players[(self.firstid+1)%3].role = 'nongmin'
                self.players[(self.firstid+2)%3].role = 'dizhu'
                self.players[(self.firstid+2)%3].state = 'playing'
                self.players[(self.firstid+2)%3].card_left.extend(self.cards_pool[3])
                #self.players[(self.firstid+2)%3].card_left.sort()
    def Play(self, playerid, cards):
        self.publicmessage = self.players[playerid].name+'出了'
        if len(self.outcard_log)>0:
            if self.outcard_log[-1][0]==playerid:
                self.outcard_log.append([playerid, cards])
                for each in cards:
                    for i in range(len(self.players[playerid].card_left)):
                        if self.players[playerid].card_left[i]==each:
                            self.players[playerid].card_left.pop(i)
                            break
                if self.players[playerid].card_left==[]:
                    self.Win(playerid)
                else:
                    self.players[playerid].state = 'waiting'
                    self.players[(playerid+1)%3].state = 'playing'
            else:
                b, t = cards_greater(cards, self.outcard_log[-1][1])
                if b:
                    self.outcard_log.append([playerid, cards])
                    for each in cards:
                        for i in range(len(self.players[playerid].card_left)):
                            if self.players[playerid].card_left[i]==each:
                                self.players[playerid].card_left.pop(i)
                                break
                    if self.players[playerid].card_left==[]:
                        self.Win(playerid)
                    else:
                        self.players[playerid].state = 'waiting'
                        self.players[(playerid+1)%3].state = 'playing'
                else:
                    self.publicmessage = self.players[playerid].name+'，你出的牌有点小'
        else:
            self.outcard_log.append([playerid, cards])
            for each in cards:
                for i in range(len(self.players[playerid].card_left)):
                    if self.players[playerid].card_left[i]==each:
                        self.players[playerid].card_left.pop(i)
                        break
            if self.players[playerid].card_left==[]:
                self.Win(playerid)
            else:
                self.players[playerid].state = 'waiting'
                self.players[(playerid+1)%3].state = 'playing'
    
    def Pass(self, playerid):
        self.publicmessage = self.players[playerid].name+'8出'
        self.players[playerid].state = 'waiting'
        self.players[(playerid+1)%3].state = 'playing'

    def Win(self, playerid):
        self.publicmessage = self.players[playerid].name+'赢了'
        self.players[playerid].state = 'win'
        if self.players[(playerid+1)%3].role==self.players[playerid].role:
            self.players[(playerid+1)%3].state = 'win'
        else:
            self.players[(playerid+1)%3].state = 'loss'
        if self.players[(playerid+2)%3].role==self.players[playerid].role:
            self.players[(playerid+2)%3].state = 'win'
        else:
            self.players[(playerid+2)%3].state = 'loss'
    
    def IsOver(self, playerid):
        self.publicmessage = self.players[playerid].name+'退出了游戏'
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

'''
url:/,/login
method:get
return:index.html
'''

@app.route('/')
@app.route('/login')
def indexpage():
    return render_template('index.html')

'''
url:/play
method:post
data:{'roomname':房间名,'playername':用户名}
return:play.html
'''

@app.route('/play', methods=['POST'])
def login():
    roomname = request.form['roomname']
    playername = request.form['playername']
    roomid = FindRoombyName(roomname)
    if roomid<0 :#房间不存在，创建新房
        newroomid = CreateRoom(roomname)
        newplayer = Player(playername)
        newplayerid = room_list[newroomid].AddPlayer(newplayer)
        return render_template('play.html', 
                                roomname=roomname, 
                                roomid=newroomid, 
                                playername=playername, 
                                playerid=newplayerid, 
                                result='登录成功')
    else:
        playerid = room_list[roomid].FindPlayerbyName(playername)
        if playerid < 0:
            if room_list[roomid].IsFull():
                return render_template('play.html', 
                                roomname='-1', 
                                roomid='-1',  
                                playername='-1', 
                                playerid='-1', 
                                result='此房已满')
            else:
                newplayer = Player(playername)
                newplayerid = room_list[roomid].AddPlayer(newplayer)
                return render_template('play.html', 
                                roomname=roomname, 
                                roomid=roomid, 
                                playername=playername, 
                                playerid=newplayerid, 
                                result='登录成功')
        else:
            return render_template('play.html', 
                                roomname=roomname, 
                                roomid=roomid, 
                                playername=playername, 
                                playerid=playerid, 
                                result='您已存在')

'''
url:/ready
method:post
data:{'roomid':房间名,'playerid':用户名}
return:json
'''

@app.route('/ready', methods=['POST'])
def getready():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])
    room_list[roomid].players[playerid].state = 'ready'

    if room_list[roomid].IsReady(playerid):
        room_list[roomid].DistributeCards()
    return jsonify({'result':'OK'})

'''
url:/grab
method:post
data:{'roomid':房间名,'playerid':用户名,'choice':'1'}//'1'抢地主，'0'不抢
return:json
'''

@app.route('/grab', methods=['POST'])
def grab():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])
    choice = request.form['choice']
    if room_list[roomid].players[playerid].state=='grabbing on turn':
        room_list[roomid].GrabDiZhu(playerid, choice)
    return jsonify({'result':'OK'})

'''
url:/out
method:post
data:{'roomid':房间名,'playerid':用户名,'cards':出的牌}//cards是形如[14, 140, 27, 26,]的数组
return:json
'''

@app.route('/out', methods=['POST'])
def outcard():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])
    cards = request.form['cards']
    cards = list(int(i) for i in cards[1:-1].split(','))
    b, t = check_card_type(cards)
    if b :
        if room_list[roomid].players[playerid].state=='playing':
            room_list[roomid].Play(playerid, cards)
            return jsonify({'result':'OK'})
        else:
            return jsonify({'error':'未轮到您出牌'})
    else:
        return jsonify({'error':'牌型不符合要求'})

'''
url:/pass
method:post
data:{'roomid':房间名,'playerid':用户名}
return:json
'''

@app.route('/pass', methods=['POST'])
def skip():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])
    if room_list[roomid].players[playerid].state=='playing':
        room_list[roomid].Pass(playerid)
    return jsonify({'result':'OK'})

'''
url:/quit
method:post
data:{'roomid':房间名,'playerid':用户名}
return:json
'''

@app.route('/quit', methods=['POST'])
def over():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])
    room_list[roomid].players[playerid].state = 'over'

    if room_list[roomid].IsOver(playerid):
        DestroyRoom(roomid)
    return jsonify({'result':'OK'})

'''
url:/refresh
method:post
data:{'roomid':房间名,'playerid':用户名}
return:{'roomname':房间名,
        'playername':用户名,
        'playerstate':用户状态,//'notready','ready','grabbing on turn','waiting','playing'
        'playerscore':用户分数,
        'playerrole':用户角色,//'nongmin','dizhu'
        'playercards':用户剩下的牌}//形如[14, 140, 27, 26,]的数组
'''

@app.route('/refresh', methods=['POST'])
def refresh():
    roomid = int(request.form['roomid'])
    playerid = int(request.form['playerid'])

    if len(room_list[roomid].outcard_log)>0:
        lastcards = str(room_list[roomid].outcard_log[-1][1])
    else:
        lastcards = '[]'
    
    if room_list[roomid].IsFull():
        Lplayername = room_list[roomid].players[(playerid-1)%3].name
        Lplayercardsamount = len(room_list[roomid].players[(playerid-1)%3].card_left)
        Rplayername = room_list[roomid].players[(playerid+1)%3].name
        Rplayercardsamount = len(room_list[roomid].players[(playerid+1)%3].card_left)
    else:
        Lplayername = 'None'
        Lplayercardsamount = '0'
        Rplayername = 'None'
        Rplayercardsamount = '0'
    
    return jsonify({'roomname':room_list[roomid].name,
                    'publicmessage':room_list[roomid].publicmessage,
                    'playername':room_list[roomid].players[playerid].name,
                    'playerstate':room_list[roomid].players[playerid].state,
                    'playerscore':str(room_list[roomid].players[playerid].score),
                    'playerrole':room_list[roomid].players[playerid].role,
                    'playercards':str(room_list[roomid].players[playerid].card_left),
                    'lastcards':lastcards,
                    'Lplayername':Lplayername,
                    'Lplayercardsamount':Lplayercardsamount,
                    'Rplayername':Rplayername,
                    'Rplayercardsamount':Rplayercardsamount,})

room_list = []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=114)
