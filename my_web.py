from flask import Flask, request, render_template
from guess_number import gen_number, hint_for_web

app = Flask(__name__)
# TODO: need to move this part to session to support multiple users
message_history = []  # To gather all messages received.
number = None  # To generate a random 4 digit numbers.
username = ""


# To log all messages and return with one single string.
def log(message):
    global message_history
    message_history.append(message)
    message_history_in_one_string = "<br />".join(message_history)
    return message_history_in_one_string


@app.route('/gameStart')
def game_start():
    global number, message_history, username
    username = request.args.get('username', '')
    if username != '':
        number = gen_number()
        message_history = []
        print number
        return render_template('my_web.html', hint=log("Let's play a game!"), username=username)
    else:
        return render_template('my_web.html', hint=log("username is blank"), username=username)


@app.route('/')
def hello():
    global number, message_history, username
    guess = request.args.get('number', '')
    if number is None:
        return render_template('my_web.html', hint=log("the game is not started"), username=username)
    if guess == '' or not guess.isdigit():
        return render_template('my_web.html', hint=log('Please enter numbers only!'), username=username)
    if len(list(guess)) != 4:
        return render_template('my_web.html', hint=log('Please enter 4 numbers exactly!'), username=username)

    result_str = hint_for_web(number, guess)
    if "Game ended." in result_str:
        number = None
    return render_template('my_web.html', hint=log(result_str), username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
