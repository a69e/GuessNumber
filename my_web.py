from flask import Flask, request, render_template
from guess_number import gen_number, hint_for_web

app = Flask(__name__)
message_history = []  # To gather all messages received.
number = gen_number()  # To generate a random 4 digit numbers.


# To log all messages and return with one single string.
def log(message):
    message_history.append(message)
    message_history_in_one_string = "<br />".join(message_history)
    return message_history_in_one_string


@app.route('/')
def hello():
    guess = request.args.get('number', '')
    if guess == '':
        return render_template('my_web.html', hint=log("Let's play a game!"))
    elif not guess.isdigit():
        return render_template('my_web.html', hint=log('Please enter numbers only!'))
    elif len(list(guess)) != 4:
        return render_template('my_web.html', hint=log('Please enter 4 numbers exactly!'))
    else:
        return render_template('my_web.html', hint=log(hint_for_web(number, guess)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
