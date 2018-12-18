from random import sample
from itertools import permutations

number = []  # The random number that need to guess.
ten_numbers = '0123456789'
info = {}  # Stores all guesses and their hints along the game.
counter = 1  # To count the steps.


# To generate a random 4 digit different numbers.
def gen_number(x):
    return ''.join(sample(ten_numbers, x))


# To pick x numbers from the remaining ten_numbers which hasn't been guessed yet.
def pick_x_number_from_not_used(x):
    global ten_numbers
    temp = list(ten_numbers)
    for i in info:
        for j in range(0, 4):
            if i[j] in temp:
                temp.remove(i[j])
    ten_numbers = ''.join(temp)
    return gen_number(x)


# To pick x numbers from the given set.
def pick_number_from_a_string(guess, x):
    return ''.join(sample(guess, x))


# To get the remaining numbers which have not been picked yet from an earlier pick.
def get_number_left_unpicked_from_a_guess(guess, picked):
    unpicked = []
    for i in guess:
        if i not in picked:
            unpicked.append(i)
    return ''.join(unpicked)


# To get the hint from any guess.
def hints(guess):
    global counter
    hint = [0, 0, counter]  # 1st: A, 2nd: B, 3rd: step.
    for i in range(0, 4):
        if guess[i] == number[i]:
            hint[0] += 1
        elif guess[i] in number:
            hint[1] += 1
    counter += 1
    if hint[0] == 4:
        print 'Game completed!'
        print 'Steps: ' + str(counter - 1)
    info[guess] = hint
    return guess, hint


# To return the total correct numbers for any guess, including A and B.
def AplusB(guess):
    return guess[1][0] + guess[1][1]


# To reform the number in such order: e.g. 1234 -> 1342
def let_2nd_be_4th(guess):
    return guess[0][0] + guess[0][2:4] + guess[0][1]


# To reform the number in such order: e.g. 1234 -> 1342
def let_3rd_be_4th(guess):
    return guess[0][0:2] + guess[0][3] + guess[0][2]


def pick_until_4A(remaining):
    for i in remaining:
        if hints(''.join(i))[1][0] == 4:
            break


# This function will deduct a best next guess based on previous guesses. If return type is 'list', it will return all
# best guesses as a list.
def next_best_guess(guess, return_type='string'):
    to_be_deleted = []  # To store all invalid numbers and then delete in one go.
    count = 0
    full_list = list(permutations([guess[0], guess[1], guess[2], guess[3]]))  # All possible combinations.

    print 'next_best_guess:all '
    print full_list

    # Applying '0A'+'1A0B'+'1AyB'.

    # To utilize '0A' to exclude invalid numbers ('0A' means the correct numbers did not appear at the correct position)
    for i in guess:
        for j in info:
            if i in j and info[j][0] == 0:
                index = list(j).index(i)
                for k in full_list:
                    if k[index] == i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []

    print 'next_best_guess:0A '
    print full_list

    #  To utilize '1A0B' to exclude invalid numbers ('1A0B' means the correct number is in the correct positions).
    for i in guess:
        for j in info:
            if i in j and info[j][0] == 1 and info[j][1] == 0:  # and list(j).index(i) == list(guess).index(i):
                index = list(j).index(i)
                for k in full_list:
                    if k[index] != i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []

    print 'next_best_guess:1A0B '
    print full_list

    #  To utilize '1AyB'(y>=1) to exclude invalid numbers ('1AyB' means not all the numbers are in correct positions).
    for i in info:
        if info[i][0] == 1 and info[i][1] >= 1:  # This if means the number matches with '1AyB'(y>=1)
            for j in full_list:
                for k in range(0, 4):
                    if i[k] == j[k]:
                        count += 1
                if count != 1:  # This measures how many numbers the input in full_list matches with the guess in info.
                    to_be_deleted.append(j)
                count = 0
            for l in to_be_deleted:
                full_list.remove(l)
            to_be_deleted = []

    print 'next_best_guess:1AyB '
    print full_list

    # This loop try to form a better guess such that each of the number had never been guessed in that position.
    # TODO: need to enhance.
    '''for i in guess:
        for j in info:
            if i in j:
                index = list(j).index(i)
                for k in full_list:
                    if k[index] == i:
                        to_be_deleted.append(k)
                if len(full_list) != len(to_be_deleted):
                    for l in to_be_deleted:
                        full_list.remove(l)
                to_be_deleted = []


        print 'next_best_guess:new position '
        print full_list'''

    # If there's still no second best guess, then we can conclude that all the combinations of this guess are invalid.
    if not full_list:
        return None

    # Please note that the list can contain more than 1 guess. In fact, all of them will the same new information.
    if return_type is 'list':  # Return the full available list if return_type is 'list'.
        temp = []
        for i in full_list:
            temp.append(''.join(i))
        return temp
    # So here it will just try to pick the first available number guess that is in the list, indistinguishably.
    else:
        return ''.join(full_list[0])


# Used by from_4B_to_4A(), to filter out invalid numbers for below groups: 01, 10
def filter_group110(guess1, guess2):
    to_be_deleted = []  # To store all invalid numbers and then delete in one go.
    full_list = list(permutations([guess1[0][0], guess1[0][1], guess1[0][2], guess1[0][3]]))  # All possible numbers.
    del full_list[0]  # Delete the number which has been guessed already.
    print full_list

    # guess3 is not a real guess but a deduction from guess1 and guess2.
    guess3 = let_2nd_be_4th(guess2), [1, 3]

    # Switch guess1 and guess2 depends on it is group 01 or 10.
    if guess1[1][0] == 1:
        temp = guess2
        guess2 = guess1
        guess1 = temp

    # Below 2 fors are to remove answers that contradict with guess1 because guess1 returns 0A4B.
    for i in full_list:
        if i[0] == guess1[0][0] or i[1] == guess1[0][1] or i[2] == guess1[0][2] or i[3] == guess1[0][3]:
            to_be_deleted.append(i)
    for i in to_be_deleted:
        full_list.remove(i)
    to_be_deleted = []  # To clear the list so that we can continue filtering.

    # Below all 6 ifs and the 2 fors are to remove answers that contradict with guess2 and guess3
    # because both guess1 and guess3 returns 1A3B.
    for i in full_list:
        if i[1] == guess2[0][1] and i[2] == guess2[0][2]:
            to_be_deleted.append(i)
        if i[1] == guess2[0][1] and i[3] == guess2[0][3]:
            to_be_deleted.append(i)
        if i[2] == guess2[0][2] and i[3] == guess2[0][3]:
            to_be_deleted.append(i)
        if i[1] == guess3[0][1] and i[2] == guess3[0][2]:
            to_be_deleted.append(i)
        if i[1] == guess3[0][1] and i[3] == guess3[0][3]:
            to_be_deleted.append(i)
        if i[2] == guess3[0][2] and i[3] == guess3[0][3]:
            to_be_deleted.append(i)
    for i in to_be_deleted:
        full_list.remove(i)
    return full_list


# Used by from_4B_to_4A(), to filter out invalid numbers for below groups: 00, 02, 20
def filter_group200(guess1, guess2):
    to_be_deleted = []  # To store all invalid numbers and then delete in one go.
    full_list = list(permutations([guess1[0][0], guess1[0][1], guess1[0][2], guess1[0][3]]))  # All possible numbers.
    del full_list[0]  # Delete the number which has been guessed already.
    print full_list

    # guess3 is not a real guess but a deduction from guess1 and guess2.
    guess3 = let_2nd_be_4th(guess2), [0, 4]

    # if group is 00, then guess3 will be below.
    if guess1[1][0] == 0 and guess2[1][0] == 0:
        guess3 = guess2

    # Switch guess1 and guess2 depends on it is group 02 or 20.
    if guess1[1][0] == 2:
        guess1 = guess2

    # Below 4 fors are to remove answers that contradict with guess1 and guess3 because they return 0A4B.
    for i in full_list:
        if i[0] == guess1[0][0] or i[1] == guess1[0][1] or i[2] == guess1[0][2] or i[3] == guess1[0][3]:
            to_be_deleted.append(i)
    for i in to_be_deleted:
        full_list.remove(i)

    to_be_deleted = []  # To clear the list so that we can continue filtering.

    for i in full_list:
        if i[0] == guess3[0][0] or i[1] == guess3[0][1] or i[2] == guess3[0][2] or i[3] == guess3[0][3]:
            to_be_deleted.append(i)
    for i in to_be_deleted:
        full_list.remove(i)
    return full_list


# "no_info_4B" here means there's no previous guess, all information we have is this guess of 4B.
def from_no_info_4B_to_4A():
    # First, find the guess that contains all 4 correct numbers, assigned to guess1.
    guess1 = []
    for i in info.items():
        if i[1][0] + i[1][1] == 4:
            guess1 = i

    # Second, from guess1 we take another guess guess2.
    guess2 = hints(let_2nd_be_4th(guess1))

    # Based on guess1 and guess2, 7 different groups can be formed as below.
    group = str(guess1[1][0]) + str(guess2[1][0])

    if group == '00' or group == '02' or group == '20':  # -------------------------------------------------------------
        # Under group 01 or 10, we can do a filtering to exclude the invalid numbers.
        remaining = filter_group200(guess1, guess2)

        # Now we can continue to pick the number in the remaining until we get 4A!
        pick_until_4A(remaining)

    if group == '01' or group == '10':  # ------------------------------------------------------------------------------
        # Under group 01 or 10, we can do a filtering to exclude the invalid numbers.
        remaining = filter_group110(guess1, guess2)

        # Now we can continue to pick the number in the remaining until we get 4A!
        pick_until_4A(remaining)

    if group == '11':  # -----------------------------------------------------------------------------------------------
        guess3 = hints(let_2nd_be_4th(guess2))
        if guess3[1][0] != 4:
            remaining = filter_group110(guess3, guess2)
            pick_until_4A(remaining)

    if group == '22':  # -----------------------------------------------------------------------------------------------
        guess3 = hints(let_3rd_be_4th(guess1))
        if guess3[1][0] != 4:
            guess4 = hints(let_2nd_be_4th(guess3))
            if guess4[1][0] != 4:
                hints(let_2nd_be_4th(guess4))


def from_4B_to_4A(guess, return_type='string'):  # guess[0][0], guess[0][1], guess[0][2], guess[0][3]
    to_be_deleted = []  # To store all invalid numbers and then delete in one go.
    full_list = list(permutations([guess[0][i] for i in range(0, 4)]))  # All possible combinations.
    # count is used to select those numbers of which we want to divided by different categories.
    count = 0
    print 'from_4B_to_4A:all '
    print full_list

    '''When 4 correct numbers had been collected, we can do more filtering to exclude invalid guesses.'''

    # To utilize '0A' to exclude invalid numbers ('0A' means the correct numbers did not appear at the correct position)
    for i in guess[0]:
        for j in info:
            if i in j and info[j][0] == 0:
                index = list(j).index(i)
                for k in full_list:
                    if k[index] == i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []

    print 'from_4B_to_4A:0A '
    print full_list

    #  To utilize '1A0B' to exclude invalid numbers ('1A0B' means the correct number is in the correct positions).
    for i in guess[0]:
        for j in info:
            if i in j and info[j][0] == 1 and info[j][1] == 0 and list(j).index(i) == list(guess[0]).index(i):
                index = list(j).index(i)
                for k in full_list:
                    if k[index] != i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []

    print 'from_4B_to_4A:1A0B '
    print full_list

    #  To utilize '1AyB'(y>=1) to exclude invalid numbers ('1AyB' means not all the numbers are in correct positions).
    for i in info:
        if info[i][0] == 1 and info[i][1] >= 1:  # This if means the number matches with '1AyB'(y>=1)
            for j in full_list:
                for k in range(0, 4):
                    if i[k] == j[k]:
                        count += 1
                if count != 1:  # This measures how many numbers the input in full_list matches with the guess in info.
                    to_be_deleted.append(j)
                count = 0
            for l in to_be_deleted:
                full_list.remove(l)
            to_be_deleted = []

    print 'from_4B_to_4A:1AyB '
    print full_list

    # Please note that the list can contain more than 1 guess. In fact, all of them will the same new information.
    if return_type is 'list':  # Return the full available list if return_type is 'list'.
        temp = []
        for i in full_list:
            temp.append(''.join(i))
        return temp
    # So here it will just try to pick the first available number guess that is in the list, indistinguishably.
    else:
        return ''.join(full_list[0])


# TODO: need to enhance the logic (also need to enhance pick_until_4A()).
def from_2B_to_4A(guess1, guess2):
    guess3 = hints(guess1[0][1] + guess2[0][0:3])

    if AplusB(guess3) == 3:
        guess4 = hints(next_best_guess(guess1[0][2] + guess3[0][0:3]))

        if AplusB(guess4) == 4:
            hints(next_best_guess(guess4))

        if AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][3] + guess3[0][0:3]))
            if AplusB(guess5) == 4:
                hints(next_best_guess(guess5))
            if AplusB(guess5) == 3:
                hints(next_best_guess(guess1[0][0] + guess3[0][0:3]))
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][1:3] + guess3[0][2:4]))
                if AplusB(guess6) == 4:
                    hints(next_best_guess(guess6))
                if AplusB(guess6) == 3:
                    hints(next_best_guess(guess1[0][1:3] + guess3[0][1] + guess3[0][3]))

        if AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess1[0][3] + guess3[0][0:2] + guess3[0][3]))
            if AplusB(guess5) == 4:
                hints(next_best_guess(guess5))
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][0] + guess3[0][3] + guess3[0][0:2]))
                if AplusB(guess6) == 2:
                    hints(next_best_guess(guess1[0][3] + guess3[0][0] + guess3[0][2:4]))
            if AplusB(guess5) == 2:
                hints(next_best_guess(guess1[0][0:2] + guess3[0][2:4]))
    else:
        guess4 = hints(guess2[0][1:4] + guess1[0][2])

        if AplusB(guess3) == 2 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][2:4] + guess2[0][1:3]))
            if AplusB(guess5) == 3:
                hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][1:3]))
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][1:3] + guess2[0][2:4]))
                if AplusB(guess6) == 3:
                    hints(next_best_guess(guess1[0][1:3] + guess2[0][1] + guess2[0][3]))

        if AplusB(guess3) == 2 and AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess1[0][1] + guess2[0][1:4]))
            if AplusB(guess5) == 1:
                guess6 = hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][0:2]))
                if AplusB(guess6) == 2:
                    guess7 = hints(next_best_guess(guess1[0][2:4] + guess2[0][0] + guess2[0][2]))
                    if AplusB(guess7) == 2:
                        hints(next_best_guess(guess1[0][1:3] + guess2[0][0] + guess2[0][3]))  # 1467 or 2358
                if AplusB(guess6) == 3:
                    guess7 = hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][0] + guess2[0][2]))
                    if AplusB(guess7) == 2:
                        hints(next_best_guess(guess1[0][2:4] + guess2[0][0:2]))
            if AplusB(guess5) == 2:
                hints(next_best_guess(guess1[0][0] + guess1[0][3] + guess2[0][1:3]))  # 1467 or 2358
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][0:2] + guess2[0][1] + guess2[0][3]))
                if AplusB(guess6) == 2:
                    guess7 = hints(next_best_guess(guess1[0][0:2] + guess2[0][2:4]))
                    if AplusB(guess7) == 2:
                        hints(next_best_guess(guess1[0][0] + guess1[0][3] + guess2[0][1:3]))  # 1467 or 2358
                    if AplusB(guess7) == 3:
                        hints(next_best_guess(guess1[0][1] + guess1[0][3] + guess2[0][2:4]))
                if AplusB(guess6) == 3:
                    guess7 = hints(next_best_guess(guess1[0][0:2] + guess2[0][2:4]))
                    if AplusB(guess7) == 2:
                        hints(next_best_guess(guess1[0][1] + guess1[0][3] + guess2[0][1] + guess2[0][3]))

        if AplusB(guess3) == 1 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][2:4] + guess2[0][2:4]))
            if AplusB(guess5) == 2:
                hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][1] + guess2[0][3]))
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][2:4] + guess2[0][1] + guess2[0][3]))
                if AplusB(guess6) == 2:
                    hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][2:4]))
            if AplusB(guess5) == 4:
                # TODO: May not need this guess if it's already 4A. e.g. 7843
                hints(next_best_guess(guess5[0]))

        if AplusB(guess3) == 1 and AplusB(guess4) == 2:
            hints(next_best_guess(guess1[0][0] + guess1[0][3] + guess2[0][0] + guess2[0][3]))


def from_2B_to_3B(guess):
    # Based on the following 1~2 guesses, all 12 groups are formed: 12, 13, 21, 22, 3
    guess3 = hints(pick_x_number_from_not_used(1) + guess[0][0:3])

    if AplusB(guess3) == 3:
        # This returns 2 incorrect numbers (i.e. the 3rd element) for later use by from_no_info_3B_to_4A.
        return guess3[0], guess3[1], pick_x_number_from_not_used(1) + guess[0][3]

    else:
        guess4 = hints(guess[0][1:4] + pick_x_number_from_not_used(1))

        if AplusB(guess3) == 1 and AplusB(guess4) == 3:
            # Rejoin guess4 so that can be used by from_3B_to_4B.
            # Note: '-1' is only used to tell play() that this particular case will be handled by from_3B_to_4A.
            return guess4[0][1:4] + guess4[0][0], [-1, 0, 4]

        # Below 3 ifs are special cases that will be handled by from_definite_3B_to_4A.
        # Also, only these 3 ifs returns 3 numbers, instead of 4.
        if AplusB(guess3) == 2 and AplusB(guess4) == 3:
            return guess4[0][0:2] + guess4[0][3]

        if AplusB(guess3) == 1 and AplusB(guess4) == 2:
            return guess4[0][2:4] + guess3[0][1]

        if AplusB(guess3) == 2 and AplusB(guess4) == 1:
            return guess3[0][0:2] + guess4[0][2]

        if AplusB(guess3) == 2 and AplusB(guess4) == 2:
            guess5 = hints(guess[0][2] + guess4[0][3] + guess[0][0:2])

            if AplusB(guess5) == 3:
                return guess5

            if AplusB(guess5) == 1:
                # Please note that this is NOT a guess but a deduction from guess5! So it doesn't count a step.
                return guess[0][2:4] + guess3[0][0] + guess[0][1], [0, 3, 5]

    return None


# '2B_and_2' means besides the 2 definite correct numbers, the other 2 correct numbers are both from another 1 guess.
def from_definite_2B_and_2_to_4A(guess, two_definite_correct_numbers = pick_x_number_from_not_used(2)):
    # Because there are only 2 correct numbers from first 2 guesses, so the 2 un-guessed numbers must be correct,
    # namely 'two_definite_correct_numbers' as the 2nd variable for this function.

    # two_numbers and other_two_numbers are the 4 numbers that form guess.
    two_numbers = pick_number_from_a_string(guess[0], 2)
    other_two_numbers = get_number_left_unpicked_from_a_guess(guess[0], two_numbers)

    # one_number and another_number are from two_numbers.
    one_number = pick_number_from_a_string(two_numbers, 1)
    another_number = get_number_left_unpicked_from_a_guess(two_numbers, one_number)

    # one_number_in_others and another_number_in_others are from other_two_numbers.
    one_number_in_others = pick_number_from_a_string(other_two_numbers, 1)
    another_number_in_others = get_number_left_unpicked_from_a_guess(other_two_numbers, one_number_in_others)

    # TODO: think about how to use next_best_guess().
    guess3 = hints(two_definite_correct_numbers + two_numbers)

    if AplusB(guess3) == 4:
        # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
        hints(from_4B_to_4A(guess3))

    elif AplusB(guess3) == 2:
        # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
        hints(from_4B_to_4A((two_definite_correct_numbers + other_two_numbers, [0, 0, 0])))

    elif AplusB(guess3) == 3:
        # TODO: think about how to use next_best_guess().
        guess4 = hints(two_definite_correct_numbers + one_number + one_number_in_others)
        if AplusB(guess4) == 4:
            # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
            hints(from_4B_to_4A(guess4))
        elif AplusB(guess4) == 2:
            # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
            print two_definite_correct_numbers + another_number + another_number_in_others
            hints(from_4B_to_4A((two_definite_correct_numbers + another_number + another_number_in_others, [0, 0, 0])))
        elif AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(two_definite_correct_numbers + one_number + another_number_in_others))
            if AplusB(guess5) == 4:
                hints(from_4B_to_4A(guess5))
            elif AplusB(guess5) == 2:
                hints(next_best_guess(two_definite_correct_numbers + one_number_in_others + another_number))


# '2B_and_1' means besides the 2 definite correct numbers, the other 2 correct numbers are different 2 guess (1+1).
def from_definite_2B_and_1_to_4A(guess1, guess2):
    # Because there are only 2 correct numbers from first 2 guesses, so the 2 un-guessed numbers must be correct.
    two_definite_correct_numbers = pick_x_number_from_not_used(2)

    # two_numbers and other_two_numbers are the 4 numbers that form guess1.
    two_numbers_in_guess1 = pick_number_from_a_string(guess1[0], 2)
    other_two_numbers_in_guess1 = get_number_left_unpicked_from_a_guess(guess1[0], two_numbers_in_guess1)

    # two_numbers and other_two_numbers are the 4 numbers that form guess2.
    two_numbers_in_guess2 = pick_number_from_a_string(guess2[0], 2)
    other_two_numbers_in_guess2 = get_number_left_unpicked_from_a_guess(guess2[0], two_numbers_in_guess2)

    # These 2 guesses are trying to find the correct numbers from which half.
    # TODO: think about how to use next_best_guess().
    guess_1 = hints(two_definite_correct_numbers + two_numbers_in_guess1)
    guess_2 = hints(two_definite_correct_numbers + two_numbers_in_guess2)

    if AplusB(guess_1) == 3 and AplusB(guess_2) == 3:
        two_other_correct_numbers_are_in_this_guess = two_numbers_in_guess1 + two_numbers_in_guess2
    if AplusB(guess_1) == 3 and AplusB(guess_2) == 2:
        two_other_correct_numbers_are_in_this_guess = two_numbers_in_guess1 + other_two_numbers_in_guess2
    if AplusB(guess_1) == 2 and AplusB(guess_2) == 3:
        two_other_correct_numbers_are_in_this_guess = other_two_numbers_in_guess1 + two_numbers_in_guess2
    if AplusB(guess_1) == 2 and AplusB(guess_2) == 2:
        two_other_correct_numbers_are_in_this_guess = other_two_numbers_in_guess1 + other_two_numbers_in_guess2

    from_definite_2B_and_2_to_4A((two_other_correct_numbers_are_in_this_guess, [0, 0, 0]), two_definite_correct_numbers)


# "no_info_3B" here means there's no previous guess from which we can deduct at least 2 correct numbers in this 3B.
def from_no_info_3B_to_4A(guess, guess1):
    # This if is to identify the last correct number from 2 numbers (not 4).
    if len(guess1[0]) == 4:
        # two_numbers are from guess1.
        two_numbers = pick_number_from_a_string(guess1[0], 2)
        if len(guess) == 2:
            # TODO: think about how to use next_best_guess().
            guess3 = hints(pick_x_number_from_not_used(2) + two_numbers)
        elif len(guess) == 3:
            # TODO: think about how to use next_best_guess().
            guess3 = hints(guess[2] + two_numbers)

        if AplusB(guess3) == 0:
            two_numbers = get_number_left_unpicked_from_a_guess(guess1[0], two_numbers)

    else:  # Length is equal to 2 for all other cases.
        two_numbers = pick_x_number_from_not_used(2)

    # Now the last correct number is either in one_number or in another_number.
    one_number = pick_number_from_a_string(two_numbers, 1)
    another_number = get_number_left_unpicked_from_a_guess(two_numbers, one_number)

    guess3 = hints(one_number + guess[0][0:3])

    if AplusB(guess3) == 4:
        # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
        hints(from_4B_to_4A(guess3))

    else:
        guess4 = hints(guess[0][1:4] + another_number)

        if AplusB(guess3) == 2 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess3[0][1:3] + guess4[0][2:4]))
            if AplusB(guess5) != 4:
                hints(next_best_guess(guess3[0][1] + guess4[0][1:4]))

        if AplusB(guess3) == 2 and AplusB(guess4) == 4:
            # TODO: need to enhance the logic (also need to enhance pick_until_4A()).
            hints(from_4B_to_4A(guess4))

        if AplusB(guess3) == 3 and AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess4[0][1:3] + guess3[0][2:4]))
            if AplusB(guess5) != 4:
                hints(next_best_guess(guess4[0][1] + guess3[0][1:4]))

        if AplusB(guess3) == 3 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess3[0][0] + guess4[0][0:3]))
            if AplusB(guess5) != 4:
                hints(next_best_guess(guess4[0][3] + guess3[0][1:4]))


def from_3B_to_4A(guess, guess1):
    # two_numbers and other_two_numbers are the 4 numbers that form guess1.
    two_numbers = pick_number_from_a_string(guess1[0], 2)
    other_two_numbers = get_number_left_unpicked_from_a_guess(guess1[0], two_numbers)

    # one_number and another_number are from two_numbers.
    one_number = pick_number_from_a_string(two_numbers, 1)
    another_number = get_number_left_unpicked_from_a_guess(two_numbers, one_number)

    # one_number_in_others and another_number_in_others are from other_two_numbers.
    one_number_in_others = pick_number_from_a_string(other_two_numbers, 1)
    another_number_in_others = get_number_left_unpicked_from_a_guess(other_two_numbers, one_number_in_others)

    # Continues from from_2B_to_3B(), so here start with guess6.
    guess6 = hints(next_best_guess(guess[0][1:3] + two_numbers))

    if AplusB(guess6) == 2:
        temp = next_best_guess(guess[0][0:3] + one_number_in_others)
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            guess7 = hints(next_best_guess(guess[0][0:3] + another_number_in_others))
            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                hints(from_4B_to_4A(guess7))
            if AplusB(guess7) == 2:
                hints(from_4B_to_4A(guess[0][1:4] + one_number_in_others))
        else:
            guess7 = hints(temp)

            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                remaining = from_4B_to_4A(guess7, 'list')
                # Now it's time to get all remaining possible answers and guess 1 by 1.
                for i in remaining:
                    hints(i)

            if AplusB(guess7) == 3:
                guess8 = hints(next_best_guess(guess[0][0:3] + another_number_in_others))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    hints(from_4B_to_4A(guess8))
                if AplusB(guess8) == 2:
                    hints(from_4B_to_4A((guess[0][1:4] + one_number_in_others, [0, 4, 8])))

            if AplusB(guess7) == 2:
                guess8 = hints(next_best_guess(guess[0][1:4] + another_number_in_others))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    hints(from_4B_to_4A(guess8))

    if AplusB(guess6) == 3:
        temp = next_best_guess(guess[0][0:3] + one_number)
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            guess7 = hints(next_best_guess(guess[0][0:3] + another_number))
            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                hints(from_4B_to_4A(guess7))
            if AplusB(guess7) == 2:
                hints(from_4B_to_4A(guess[0][1:4] + one_number))
        else:
            guess7 = hints(temp)

            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                remaining = from_4B_to_4A(guess7, 'list')
                # Now it's time to get all remaining possible answers and guess 1 by 1.
                for i in remaining:
                    hints(i)

            if AplusB(guess7) == 3:
                guess8 = hints(next_best_guess(guess[0][0:3] + another_number))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    hints(from_4B_to_4A(guess8))
                if AplusB(guess8) == 2:
                    hints(from_4B_to_4A((guess[0][1:4] + one_number, [0, 4, 8])))

            if AplusB(guess7) == 2:
                guess8 = hints(next_best_guess(guess[0][1:4] + another_number))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    hints(from_4B_to_4A(guess8))


# "definite_3B" here means the 3 correct numbers had been confirmed.
# The variable 'three' here contains and only contain all 3 correct numbers.
def from_definite_3B_to_4A(three, guess):
    # two_numbers and other_two_numbers are the 4 numbers that form guess.
    two_numbers = pick_number_from_a_string(guess[0], 2)
    other_two_numbers = get_number_left_unpicked_from_a_guess(guess[0], two_numbers)

    # one_number and another_number are from two_numbers.
    one_number = pick_number_from_a_string(two_numbers, 1)
    another_number = get_number_left_unpicked_from_a_guess(two_numbers, one_number)

    # one_number_in_others and another_number_in_others are from other_two_numbers.
    one_number_in_others = pick_number_from_a_string(other_two_numbers, 1)
    another_number_in_others = get_number_left_unpicked_from_a_guess(other_two_numbers, one_number_in_others)

    guess5 = hints(next_best_guess(three[0:2] + two_numbers))

    if AplusB(guess5) == 2:
        temp = next_best_guess(three + one_number_in_others)
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            hints(next_best_guess(three + another_number_in_others))
        else:
            guess6 = hints(next_best_guess(temp))
            if AplusB(guess6) == 3:
                hints(next_best_guess(three + another_number_in_others))

    if AplusB(guess5) == 3:
        temp = next_best_guess(three + one_number)
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            hints(next_best_guess(three + another_number))
        else:
            guess6 = hints(next_best_guess(temp))
            if AplusB(guess6) == 3:
                hints(next_best_guess(three + another_number))


def play():
    # Based on the first 1~2 guesses, all 12 groups are: 02, 03, 04, 11, 12, 13, 20, 21, 22, 30, 31, 4
    guess1 = hints('1234')
    # guess1 = hints(gen_number())

    # Similar algorithm for group 4 & 04 ---------------------------------------
    if AplusB(guess1) == 4:
        if guess1[1][0] != 4:
            from_no_info_4B_to_4A()
    else:
        guess2 = hints('5678')
        # guess2 = hints(pick_x_number_not_used(4))

    if AplusB(guess1) == 0 and AplusB(guess2) == 4:
        from_no_info_4B_to_4A()

    # Similar algorithm for group 02 & 20 & 11 ---------------------------------------
    if AplusB(guess1) == 1 and AplusB(guess2) == 1:
        from_definite_2B_and_1_to_4A(guess1, guess2)

    if AplusB(guess1) == 0 and AplusB(guess2) == 2:
        from_definite_2B_and_2_to_4A(guess2)
        
    if AplusB(guess1) == 2 and AplusB(guess2) == 0:
        from_definite_2B_and_2_to_4A(guess1)

    # Similar algorithm for group 03 & 30 & 13 & 31 ---------------------------------------
    if AplusB(guess1) == 0 and AplusB(guess2) == 3:
        from_no_info_3B_to_4A(guess2, pick_x_number_from_not_used(2))

    if AplusB(guess1) == 3 and AplusB(guess2) == 0:
        from_no_info_3B_to_4A(guess1, pick_x_number_from_not_used(2))

    if AplusB(guess1) == 1 and AplusB(guess2) == 3:
        from_no_info_3B_to_4A(guess2, guess1)

    if AplusB(guess1) == 3 and AplusB(guess2) == 1:
        from_no_info_3B_to_4A(guess1, guess2)

    # Similar algorithm for group 12 & 21 ---------------------------------------
    if AplusB(guess1) == 1 and AplusB(guess2) == 2:
        three_b = from_2B_to_3B(guess2)

        # 3 different cases to reach 4A, each deducted with a different functions(no_info, definite and normal).
        if len(info) == 3:
            from_no_info_3B_to_4A(three_b, guess1)
        elif len(info) == 4 and three_b[1][0] != -1:  # This '-1' is a flag, only take care group '13' in from_2B_to_3B.
            from_definite_3B_to_4A(three_b, guess1)
        else:
            from_3B_to_4A(three_b, guess1)

    if AplusB(guess1) == 2 and AplusB(guess2) == 1:
        three_b = from_2B_to_3B(guess1)

        # 3 different cases to reach 4A, each deducted with a different functions(no_info, definite and normal).
        if len(info) == 3:
            from_no_info_3B_to_4A(three_b, guess2)
        elif len(info) == 4 and three_b[1][0] != -1:
            from_definite_3B_to_4A(three_b, guess2)
        else:
            from_3B_to_4A(three_b, guess2)

    if AplusB(guess1) == 2 and AplusB(guess2) == 2:
        from_2B_to_4A(guess1, guess2)


if __name__ == '__main__':
    number = '8523'
    play()
    print info
