from flask import Flask, session, render_template, request, redirect, g, url_for
import os
from collections import OrderedDict
import csv
import threading
import time
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = os.urandom(24)
# allow update for images
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


gold = {}
factory = {}
earning = {}
worth = {}
users = {}
messages = {}
drugs = {}
defattack = {}

def readfiles():
    global worth
    global factory
    global gold
    global users
    global earning
    global messages
    global drugs
    global defattack
    with open('users.txt', 'r') as csvfile:
        users = eval(csvfile.read())

    with open('gold.txt', 'r') as csvfile:
        gold = eval(csvfile.read())

    with open('earning.txt', 'r') as csvfile:
        earning = eval(csvfile.read())

    with open('factory.txt', 'r') as csvfile:
        factory = eval(csvfile.read())

    with open('worth.txt', 'r') as csvfile:
        worth = eval(csvfile.read())

    with open('messages.txt', 'r') as csvfile:
        messages = eval(csvfile.read())
    
    with open('drugs.txt', 'r') as csvfile:
        drugs = eval(csvfile.read())

    with open('defattack.txt', 'r') as csvfile:
        defattack = eval(csvfile.read())


def writefiles():
    global worth
    global factory
    global gold
    global users
    global earning
    global messages
    global drugs
    global defattack
    with open('gold.txt', 'w') as csvfile:
        csvfile.write('%s'%(gold))
    with open('earning.txt', 'w') as csvfile:
        csvfile.write('%s'%(earning))
    with open('factory.txt', 'w') as csvfile:
        csvfile.write('%s'%(factory))
    with open('users.txt', 'w') as csvfile:
        csvfile.write('%s'%(users))
    with open('worth.txt', 'w') as csvfile:
        csvfile.write('%s'%(worth))
    with open('messages.txt', 'w') as csvfile:
        csvfile.write('%s'%(messages))
    with open('drugs.txt', 'w') as csvfile:
        csvfile.write('%s'%(drugs))
    with open('defattack.txt', 'w') as csvfile:
        csvfile.write('%s'%(defattack))


def update_worth():
    global worth
    global factory
    global gold
    global defattack
    for i in worth:
        worth[i] = int(factory[i])*100 + int(gold[i])
    for i in defattack:
        defattack[i]['base'] = [0,0]
        for j in defattack[i]:
            defattack[i]['base'][0] += defattack[i][j][0]
            defattack[i]['base'][1] += defattack[i][j][1]





def update_all():
    update_worth()
    writefiles()
    readfiles()


def reset_msg():
    global messages
    for i in messages:
        messages[i] = []
    writefiles()
    readfiles()


readfiles()
update_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        password = str(request.form['password'])
        username = str(request.form['username'])
        try:
            if users[username] == password:
                session['user'] = request.form['username']
                return redirect(url_for('protected'))
            else:
                return render_template('index.html', msg = 'Wrong password')
        except:
            return render_template('index.html', msg = 'Wrong password')

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    global users
    global gold
    global factory
    global earning
    global worth
    global messages
    if request.method == 'POST':
        session.pop('user', None)

        password = str(request.form['password'])
        username = str(request.form['username'])

        if username not in users:
            users[username] = password
            factory[username] = 1
            gold[username] = 1000
            earning[username] = 30
            messages[username] = []
            defattack[username] = {'base':[0,0]}
            drugs[username] = {}
            worth[username] = int(factory[username])*100 + int(gold[username])
            update_all()
            #reset_msg()
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/protected', methods=['GET', 'POST'])
def protected():
    D1 = dict(OrderedDict(sorted(worth.items(), key = lambda t: t[1], reverse = True)))
    ranking = [x for x in D1]
    number1image = 'blanc.jpg'
    if g.user:
        readfiles()
        update_all()
        
        #def items, base:[def,atk]-> [ITEM][def,atk,picture.jpg,description,0 head, 1 left arm, 2 right arm, 3 chest, 4 pants, 5 boots]


        helmet = ['','']
        for i in defattack[session['user']]:
            if i == 'base':
                continue
            else:
                try:
                    # HELMET
                    if defattack[session['user']][i][4] == 0:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        helmet = [pic,desc]
                    
                    # left arm
                    if defattack[session['user']][i][4] == 1:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        left_arm = [pic,desc]

                    # right arm
                    if defattack[session['user']][i][4] == 2:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        right_arm = [pic,desc]

                    
                    # chest
                    if defattack[session['user']][i][4] == 3:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        chest = [pic,desc]

                    # pants
                    if defattack[session['user']][i][4] == 4:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        pants = [pic,desc]

                    # boots
                    if defattack[session['user']][i][4] == 4:
                        # defe = defattack[session['user']][0]
                        # attacke = defattack[session['user']][1]
                        pic = defattack[session['user']][i][2]
                        desc = defattack[session['user']][i][3]
                        boots = [pic,desc]
                except:
                    print('nothing')

                else:
                    print('nothing')

        update_all()
        if session['user'] == ranking[0]:
            number1image = 'gold.jpg'
        if request.method == 'POST':
            buy = request.form['amount']
            if int(buy)*100 <= gold[session['user']]:
                gold[session['user']] -= int(buy)*100
                factory[session['user']] += int(buy)
                earning[session['user']] += int(buy)*30
                update_all()

                return render_template('protected.html', username = session['user'], gold = gold[session['user']],\
                 factory = factory[session['user']], earning = earning[session['user']], messages = messages[session['user']], \
                 gold_1st = number1image, defence = defattack[session['user']]['base'][0],attack = defattack[session['user']]['base'][1], helmet = helmet)
            else:
                return render_template('protected.html', username = session['user'], gold = gold[session['user']], \
                factory = factory[session['user']], earning = earning[session['user']], msg = 'You cant afford this!', messages = messages[session['user']], \
                gold_1st = number1image, defence = defattack[session['user']]['base'][0], attack = defattack[session['user']]['base'][1], helmet = helmet)
        else:
            return render_template('protected.html', username = session['user'], gold = gold[session['user']], \
            factory = factory[session['user']], earning = earning[session['user']], messages = messages[session['user']], \
            gold_1st = number1image, defence = defattack[session['user']]['base'][0],attack = defattack[session['user']]['base'][1], helmet = helmet)
    else:
        return redirect(url_for('index'))



@app.route('/lb')
def lead():
    global worth
    if g.user:
        D1 = dict(OrderedDict(sorted(worth.items(), key = lambda t: t[1], reverse = True)))
        return render_template('lb.html', leadboard = D1)

    return redirect(url_for('index'))





@app.route('/drug', methods=['GET', 'POST'])
def drug_store():
    if g.user:
        l = [x for x in np.random.random(20)]
        plt.plot(l)
        plt.savefig('static/1.png')
        plt.close()
        return render_template('drugs.html',cocaine = '1')
    else:
        return redirect(url_for('index'))



@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'You have logged out'



ticker = 0
timelock = 0
def wage():
    global ticker
    global timelock
    if time.localtime()[4] != ticker and timelock == 1:
        timelock = 0
        time.sleep(10)
    if time.localtime()[4] == ticker and timelock == 0:
        timelock = 1
        global gold
        global factory
        global messages
        print('Wages: %s'%time.localtime()[4])
        for user in earning:
            gold[user] += earning[user]
            value_gained = earning[user]
            messages[user].append('%s:%s| Earned %d gold from factories.'%(time.localtime()[3],time.localtime()[4],value_gained))
        update_all()
    else:
        time.sleep(10)
    wage()



thread = threading.Thread(target = wage)
thread.start()
