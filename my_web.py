from flask import Flask, request, render_template, session
from my_db import crud, show
import guess_number
import time


app = Flask(__name__)
app.secret_key = 'diudiudiu'


# To log new message and append it to all old messages and then return with one single string.
def log(message):
    message_history = session['message_history_in_one_string'].split('<br />')
    message_history.append(message)
    session['message_history_in_one_string'] = '<br />'.join(message_history)
    return session['message_history_in_one_string']


# To convert the guess number and result list into one single string.
def convert(guess, result):
    return str(guess) + " : " + "".join(result)


@app.route('/login')
def login():
    if request.args.get('username', '') == '':
        return render_template('login.html', error='Name cannot be blank!')
    session['username'] = request.args.get('username', '')
    session['number'] = None
    session['counter'] = 0
    session['message_history_in_one_string'] = ''
    return render_template('my_web.html', hint=log('Welcome to the number guess game! '
                                                   'Please click "New game!" to start a new game.'),
                           welcome='Welcome, %s!' % session['username'])


@app.route('/gameStart')
def game_start():
    if 'username' in session:
        session['number'] = guess_number.gen_number()
        print session['number']
        return render_template('my_web.html', hint=log("Let's play a game!"),
                               welcome='Welcome, %s!' % session['username'])
    else:
        return render_template('login.html')


@app.route('/')
def play():
    if 'username' not in session:
        return render_template('login.html')

    if session['number'] is None:
        return render_template('my_web.html', hint=log('Game has not started yet!'),
                               welcome='Welcome, %s!' % session['username'])

    guess = request.args.get('number', '')
    if guess == '' or not guess.isdigit():
        return render_template('my_web.html', hint=log('Please enter numbers only!'),
                               welcome='Welcome, %s!' % session['username'])
    if len(list(guess)) != 4:
        return render_template('my_web.html', hint=log('Please enter 4 numbers exactly!'),
                               welcome='Welcome, %s!' % session['username'])
    if len(list(guess)) != len(set(list(guess))):
        return render_template('my_web.html', hint=log('Please enter 4 different numbers!'),
                               welcome='Welcome, %s!' % session['username'])

    result = guess_number.hint(session['number'], guess, session['counter'])
    if result[0] == '4' and result[2] == '0':
        # To insert a record of the total guesses of this game, plus timestamp.
        crud('insert', [session['username'], session['counter'], time.strftime('%Y%m%d %H:%M', time.localtime())])
        show()
        session['number'] = None
        session['counter'] = 0
        return render_template('my_web.html', hint=log(convert(guess, result) +
                                                       '<br />You are amazing!<br />Game ended.'),
                               welcome='Welcome, %s!' % session['username'])
    return render_template('my_web.html', hint=log(convert(guess, result)),
                           welcome='Welcome, %s!' % session['username'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
