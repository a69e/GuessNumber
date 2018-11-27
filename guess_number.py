import random


def gen_number():
    return random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)


def take_a_guess():
    while True:
        guess = raw_input('enter 4 numbers:')
        if not guess.isdigit():
            print 'enter numbers only'
        elif len(list(guess)) != 4:
            print 'enter 4 numbers only'
        else:
            return list(guess)


def hint(number, guess):
    result = [0, 'A', 0, 'B']
    for i in range(0, 4):
        if guess[i] == number[i]:
            result[0] += 1
        elif guess[i] in number:
            result[2] += 1
    print str(result[0]) + result[1] + str(result[2]) + result[3]
    return result


def hint_for_web(number, guess):
    result = [0, 'A', 0, 'B']
    for i in range(0, 4):
        if guess[i] == number[i]:
            result[0] += 1
        elif guess[i] in number:
            result[2] += 1
    result[0] = str(result[0])
    result[2] = str(result[2])
    if result[0] == '4' and result[2] == '0':
        return str(guess) + " : " + "".join(result) + "<br />You are amazing!<br />Game ended."
    else:
        return str(guess) + " : " + "".join(result)


def game_start():
    number = gen_number()
    while True:
        result = hint(number, take_a_guess())
        if result[0] == 4 and result[2] == 0:
            print 'You are amazing!'
            break


if __name__ == '__main__':
    game_start()
