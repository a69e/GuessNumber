import random


number = []
counter = 0
ten_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
available_answers = [a + b + c + d for a in ten_numbers for b in ten_numbers for c in ten_numbers for d in ten_numbers
                     if a != b and a != c and a != d and b != c and b != d and c != d]
available_hints = ['0A0B', '0A1B', '0A2B', '0A3B', '0A4B', '1A0B', '1A1B',
                   '1A2B', '1A3B', '2A0B', '2A1B', '2A2B', '3A0B', '4A0B']
hint0 = ['0A0B']
hint1 = ['0A1B', '1A0B']
hint2 = ['0A2B', '1A1B', '2A0B']
hint3 = ['0A3B', '1A2B', '2A1B', '3A0B']
hint4 = ['0A4B', '1A3B', '2A2B', '4A0B']


def gen_number():
    return random.sample(ten_numbers, 4)


def get_hint(guess):
    global counter
    hint = [0, 'A', 0, 'B']
    counter += 1
    for i in range(0, 4):
        if list(guess)[i] == number[i]:
            hint[0] += 1
        elif guess[i] in number:
            hint[2] += 1
    for i in range(0, 4):
        if i % 2 == 0:
            hint[i] = str(hint[i])
    return hint


def narrow_down_answer(hint):
    hint = ''.join(hint)
    current_guess = available_answers[0]
    to_be_deleted = []
    if hint in hint0:
        for i in current_guess:
            for j in available_answers:
                if i in j:
                    to_be_deleted.append(j)
            for k in to_be_deleted:
                available_answers.remove(k)
                to_be_deleted = []
    if hint in hint1:
        print hint
    if hint in hint2:
        print hint
    if hint in hint3:
        print hint
    if hint in hint4:
        print hint
        if hint in hint4:
            pass


def find_number():
    if len(available_answers) == 1:
        print available_answers
    narrow_down_answer(get_hint(available_answers[0]))
    return find_number()


if __name__ == '__main__':
    number = gen_number()
    narrow_down_answer('0A4B')
    print available_answers
