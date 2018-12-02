from flask import Flask, request, render_template, session
from my_db import crud, show
import guess_number
import time


app = Flask(__name__)
app.secret_key = 'diudiudiu'
# TODO: need to move this part to session to support multiple users
message_history = []  # To gather all messages received.


# To log all messages and return with one single string.
def log(message):
    global message_history
    message_history.append(message)
    message_history_in_one_string = "<br />".join(message_history)
    return message_history_in_one_string


# To convert the guess number and result list into one single string.
def convert(guess, result):
    return str(guess) + " : " + "".join(result)


@app.route('/login')
def login():
    session['username'] = request.args.get('username', '')
    return render_template('my_web.html', welcome='Welcome, %s!' % session['username'])


@app.route('/gameStart')
def game_start():
    global message_history
    if 'username' in session:
        guess_number.number = guess_number.gen_number()
        message_history = []
        print guess_number.number
        return render_template('my_web.html', hint=log("Let's play a game!"),
                               welcome='Welcome, %s!' % session['username'])
    else:
        return render_template('login.html')


@app.route('/')
def play():
    global message_history
    if 'username' not in session:
        return render_template('login.html')

    if guess_number.number is None:
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

    result = guess_number.hint(guess_number.number, guess)
    if result[0] == '4' and result[2] == '0':
        # To insert a record of the total guesses of this game, plus timestamp.
        crud('insert', [session['username'], guess_number.counter, time.strftime('%Y%b%d %H:%M', time.localtime())])
        show()
        guess_number.number = None
        guess_number.counter = 0
        return render_template('my_web.html', hint=log(convert(guess, result) +
                                                       '<br />You are amazing!<br />Game ended.'),
                               welcome='Welcome, %s!' % session['username'])
    return render_template('my_web.html', hint=log(convert(guess, result)),
                           welcome='Welcome, %s!' % session['username'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
