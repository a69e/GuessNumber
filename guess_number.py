import random

number = None  # To generate a random 4 digit numbers.


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


def hint(answer, guess, counter):
    counter = int(counter)
    counter += 1
    result = [0, 'A', 0, 'B', str(counter)]
    for i in range(0, 4):
        if guess[i] == answer[i]:
            result[0] += 1
        elif guess[i] in answer:
            result[2] += 1
    for i in range(0, 4):
        if i % 2 == 0:
            result[i] = str(result[i])
    # The print result is only used in local game but not web game.
    # print str(result[0]) + result[1] + str(result[2]) + result[3] + str(result[4])
    return result


def game_start():
    answer = gen_number()
    while True:
        result = hint(answer, take_a_guess(), 0)
        if result[0] == 4 and result[2] == 0:
            print 'You are amazing!'
            break


if __name__ == '__main__':
    game_start()
