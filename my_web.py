from flask import Flask, request, render_template
import guess_number

app = Flask(__name__)
# TODO: need to move this part to session to support multiple users
message_history = []  # To gather all messages received.
username = ""


# To log all messages and return with one single string.
def log(message):
    global message_history
    message_history.append(message)
    message_history_in_one_string = "<br />".join(message_history)
    print message_history
    return message_history_in_one_string


@app.route('/gameStart')
def game_start():
    global message_history, username
    username = request.args.get('username', '')
    if username != '':
        guess_number.number = guess_number.gen_number()
        message_history = []
        print guess_number.number
        return render_template('my_web.html', hint=log("Let's play a game!"), username=username)
    else:
        return render_template('my_web.html', hint=log("Username is blank!"), username=username)


@app.route('/')
def hello():
    global message_history, username
    guess = request.args.get('number', '')
    if guess_number.number is None:
        return render_template('my_web.html', hint=log("Game hasn't started yet. Please enter your name to start "
                                                       "a new game."), username=username)
    if guess == '' or not guess.isdigit():
        return render_template('my_web.html', hint=log('Please enter numbers only!'), username=username)
    if len(list(guess)) != 4:
        return render_template('my_web.html', hint=log('Please enter 4 numbers exactly!'), username=username)
    if len(list(guess)) != len(set(list(guess))):
        return render_template('my_web.html', hint=log('Please enter 4 different numbers!'), username=username)

    result_str = guess_number.hint_for_web(guess_number.number, guess)
    if "Game ended." in result_str:
        guess_number.number = None
        guess_number.counter = 0
    return render_template('my_web.html', hint=log(result_str), username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
