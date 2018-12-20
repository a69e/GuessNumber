from random import sample
from itertools import permutations
import time

number = []  # The random number that need to guess.
ten_numbers = '0123456789'
info = {}  # Stores all guesses and their hints along the game.
counter = 0  # To count the steps.
success = 0  # To count the successful game for multiple game plays, and display the outcome.


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
    global counter, success
    counter += 1
    hint = [0, 0, counter]  # 1st: A, 2nd: B, 3rd: step.
    for i in range(0, 4):
        if guess[i] == number[i]:
            hint[0] += 1
        elif guess[i] in number:
            hint[1] += 1
    if hint[0] == 4:
        success += 1
        print 'Game completed!'
        print 'Steps: ' + str(counter)
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


# This handles those guesses which contains all 4 correct numbers but you may still need to guess 2 or more times.
def from_4B_to_4A(guess):
    # To unify the format of guess.
    if len(guess) == 2:
        guess = guess[0]

    # To make sure not to guess the same number a second time.
    remaining = next_best_guess(guess, 'list')
    count = 0
    for i in remaining:
        for j in info:
            for k in range(0, 4):
                if i[k] == j[k]:
                    count += 1
            if count == 4:
                remaining.remove(i)
            count = 0

    # The reason here we make another guess and update the remaining list accordingly b4 using the loop below,
    # is to make sure to avoid duplicate/multiple guesses which are unnecessary.
    if hints(remaining[0])[1][0] != 4:
        # To make sure once again not to guess the same number a second time.
        remaining = next_best_guess(guess, 'list')
        count = 0
        for i in remaining:
            for j in info:
                for k in range(0, 4):
                    if i[k] == j[k]:
                        count += 1
                if count == 4:
                    remaining.remove(i)
                count = 0

        # To pick the guess in the remaining possible set until reach 4A.
        for i in remaining:
            if hints(''.join(i))[1][0] == 4:
                break


# Below 4 functions (filter_group110(), filter_group200(), guess_until_4A() and from_no_info_4B_to_4A())
# only solves one particular case , so that the logic is somehow different from other functions.
# This is the earliest written function, so it is a bit out of order and of low efficiency. :)
# TODO: Can be integrated into the same other logic (e.g. next_best_guess()) later on.

# Only used by from_no_info_4B_to_4A(), to filter out invalid numbers for below groups: 01, 10
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


# Only used by from_no_info_4B_to_4A(), to filter out invalid numbers for below groups: 00, 02, 20
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


def guess_until_4A(remaining):
    next_best_guess(remaining[0], 'string', remaining)
    for i in remaining:
        if hints(''.join(i))[1][0] == 4:
            break


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
        guess_until_4A(filter_group200(guess1, guess2))

    if group == '01' or group == '10':  # ------------------------------------------------------------------------------
        # Under group 01 or 10, we can do a filtering to exclude the invalid numbers.
        guess_until_4A(filter_group110(guess1, guess2))

    if group == '11':  # -----------------------------------------------------------------------------------------------
        guess3 = hints(let_2nd_be_4th(guess2))
        if guess3[1][0] != 4:
            guess_until_4A(filter_group110(guess3, guess2))

    if group == '22':  # -----------------------------------------------------------------------------------------------
        guess3 = hints(let_3rd_be_4th(guess1))
        if guess3[1][0] != 4:
            guess4 = hints(let_2nd_be_4th(guess3))
            if guess4[1][0] != 4:
                hints(let_2nd_be_4th(guess4))


'''******************************************************************************************************************'''


# This function will deduct a best next guess based on previous guesses.
# If return type is 'list', it will return all best guesses in a list.
# Also, please note that it will try to apply filter rules 1 by 1.
# If after applying a rule will return an empty list, then it will roll back and skip applying that rule.
# This is just to make sure that the return is always non-empty, so as to carry on the remaining steps.
# TODO: Having said that, the game steps will be smaller if we can figure a way to improve the logic.
def next_best_guess(guess, return_type='string', remaining=None):
    to_be_deleted = []  # To store all invalid numbers and then delete in one go.
    possible_list = [guess, ]  # To store all possible combinations after filtering some rules, only if it is non-empty.
    full_list = list(permutations([guess[i] for i in range(0, 4)]))  # All possible combinations.
    count = 0

    # We've added a new handling here especially for from_no_info_4B_to_4A().
    if remaining is not None:
        possible_list = remaining
        full_list = remaining

    # for testing purpose:
    # print 'next_best_guess:all '
    # print full_list
    # print possible_list

    # Applying rules below 1 by 1: '0A'+'1A0B'+'1AyB'+'2AyB'+'3AyB'.

    # To utilize '0A' to exclude invalid numbers ('0A' means the correct numbers did not appear at the correct position)
    for i in guess:
        for j in info:
            if i in j and info[j][0] == 0:  # Meaning this number j matches with '0A'
                index = list(j).index(i)
                for k in full_list:
                    if k[index] == i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []
    if full_list:
        possible_list = tuple(full_list)  # It will update(truncate) possible_list if full_list is not empty.
    else:
        full_list = list(possible_list)  # Roll back full_list to previous non-empty set to avoid it becomes empty.

    # To utilize '1A0B' to exclude invalid numbers ('1A0B' means the correct number is in the correct positions).
    for i in guess:
        for j in info:
            if i in j and info[j][0] == 1 and info[j][1] == 0:  # Meaning this number j matches with '1A0B'
                index = list(j).index(i)
                for k in full_list:
                    if k[index] != i:
                        to_be_deleted.append(k)
                for l in to_be_deleted:
                    full_list.remove(l)
                to_be_deleted = []
    if full_list:
        possible_list = tuple(full_list)  # It will update(truncate) possible_list if full_list is not empty.
    else:
        full_list = list(possible_list)  # Roll back full_list to previous non-empty set to avoid it becomes empty.

    # To utilize '1AyB'(y>=1) to exclude invalid numbers ('1AyB' means not all the numbers are in correct positions).
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
    if full_list:
        possible_list = tuple(full_list)  # It will update(truncate) possible_list if full_list is not empty.
    else:
        full_list = list(possible_list)  # Roll back full_list to previous non-empty set to avoid it becomes empty.

    # To utilize '2AyB' to exclude invalid numbers.
    # '2AyB' means there are 2 and only 2 correct numbers are in the correct positions.
    for i in info:
        if info[i][0] == 2:  # This if means the number matches with '2AyB'
            for j in full_list:
                for k in range(0, 4):
                    if i[k] == j[k]:
                        count += 1
                if count != 2:  # This measures how many numbers the input in full_list matches with the guess in info.
                    to_be_deleted.append(j)
                count = 0
            for l in to_be_deleted:
                full_list.remove(l)
            to_be_deleted = []
    if full_list:
        possible_list = tuple(full_list)  # It will update(truncate) possible_list if full_list is not empty.
    else:
        full_list = list(possible_list)  # Roll back full_list to previous non-empty set to avoid it becomes empty.

    # To utilize '3AyB' to exclude invalid numbers.
    # '3AyB' means there are 3 and only 3 correct numbers are in the correct positions.
    for i in info:
        if info[i][0] == 3:  # This if means the number matches with '3AyB'
            for j in full_list:
                for k in range(0, 4):
                    if i[k] == j[k]:
                        count += 1
                if count != 3:  # This measures how many numbers the input in full_list matches with the guess in info.
                    to_be_deleted.append(j)
                count = 0
            for l in to_be_deleted:
                full_list.remove(l)
            to_be_deleted = []
    if not full_list:
        full_list = list(possible_list)  # Roll back full_list to previous non-empty set to avoid it becomes empty.

    # Please note that the list can contain more than 1 guess. In fact, all of them will the same new information.
    if return_type is 'list':  # Return the full available list if return_type is 'list'.
        temp = []
        for i in full_list:
            temp.append(''.join(i))
        return temp
    # Below will just try to pick the first available number guess that is in the list, indistinguishably.
    else:
        return ''.join(full_list[0])


def from_2B_to_4A(guess1, guess2):
    guess3 = hints(guess1[0][1] + guess2[0][0:3])

    if AplusB(guess3) == 3:
        guess4 = hints(next_best_guess(guess1[0][2] + guess3[0][0:3]))

        if AplusB(guess4) == 4 and guess4[1][0] != 4:
            from_4B_to_4A(guess4)

        if AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][3] + guess3[0][0:3]))
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)
            if AplusB(guess5) == 3:
                from_4B_to_4A(guess1[0][0] + guess3[0][0:3])
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][1:3] + guess3[0][2:4]))
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
                if AplusB(guess6) == 3:
                    from_4B_to_4A(guess1[0][1:3] + guess3[0][1] + guess3[0][3])

        if AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess1[0][3] + guess3[0][0:2] + guess3[0][3]))
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][0] + guess3[0][3] + guess3[0][0:2]))
                if AplusB(guess6) == 2:
                    from_4B_to_4A(guess1[0][3] + guess3[0][0] + guess3[0][2:4])
            if AplusB(guess5) == 2:
                from_4B_to_4A(guess1[0][0:2] + guess3[0][2:4])
    else:
        guess4 = hints(guess2[0][1:4] + guess1[0][2])

        if AplusB(guess3) == 2 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][2:4] + guess2[0][1:3]))
            if AplusB(guess5) == 3:
                from_4B_to_4A(guess1[0][0] + guess1[0][2] + guess2[0][1:3])
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][1:3] + guess2[0][2:4]))
                if AplusB(guess6) == 3:
                    from_4B_to_4A(guess1[0][1:3] + guess2[0][1] + guess2[0][3])
                elif guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 2 and AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess1[0][1] + guess2[0][1:4]))
            if AplusB(guess5) == 1:
                guess6 = hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][0:2]))
                if AplusB(guess6) == 2:
                    from_4B_to_4A(guess1[0][2:4] + guess2[0][0] + guess2[0][2])
                if AplusB(guess6) == 3:
                    guess7 = hints(next_best_guess(guess1[0][0] + guess1[0][2] + guess2[0][0] + guess2[0][2]))
                    if AplusB(guess7) == 2:
                        from_4B_to_4A(guess1[0][2:4] + guess2[0][0:2])
                    elif guess7[1][0] != 4:
                        from_4B_to_4A(guess7)
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][1:3] + guess2[0][0] + guess2[0][3]))
                if AplusB(guess6) == 0:
                    from_4B_to_4A(guess1[0][0] + guess1[0][3] + guess2[0][1:3])
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][0:2] + guess2[0][1] + guess2[0][3]))
                if AplusB(guess6) == 2:
                    from_4B_to_4A(guess1[0][1] + guess1[0][3] + guess2[0][2:4])
                if AplusB(guess6) == 3:
                    guess7 = hints(next_best_guess(guess1[0][0:2] + guess2[0][2:4]))
                    if AplusB(guess7) == 2:
                        from_4B_to_4A(guess1[0][1] + guess1[0][3] + guess2[0][1] + guess2[0][3])
                    elif guess7[1][0] != 4:
                        from_4B_to_4A(guess7)
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 2 and AplusB(guess4) == 1:
            guess5 = hints(next_best_guess(guess1[0][0] + guess1[0][3] + guess2[0][0:2]))
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][0:2] + guess2[0][0] + guess2[0][3]))
                if AplusB(guess6) == 3:
                    from_4B_to_4A(guess1[0][1] + guess1[0][3] + guess2[0][0] + guess2[0][3])
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 3:
                from_4B_to_4A(guess1[0][0] + guess1[0][3] + guess2[0][0] + guess2[0][2])
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 1 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess1[0][2:4] + guess2[0][2:4]))
            if AplusB(guess5) == 2:
                from_4B_to_4A(guess1[0][0] + guess1[0][2] + guess2[0][1] + guess2[0][3])
            if AplusB(guess5) == 3:
                guess6 = hints(next_best_guess(guess1[0][2:4] + guess2[0][1] + guess2[0][3]))
                if AplusB(guess6) == 2:
                    from_4B_to_4A(guess1[0][0] + guess1[0][2] + guess2[0][2:4])
                elif guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5[0])

        if AplusB(guess3) == 1 and AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess1[0][0] + guess1[0][3] + guess2[0][2:4]))
            if AplusB(guess5) == 2:
                guess6 = hints(next_best_guess(guess1[0][2:4] + guess2[0][0] + guess2[0][3]))
                if AplusB(guess6) == 3:
                    from_4B_to_4A(guess1[0][0] + guess1[0][2] + guess2[0][0] + guess2[0][3])
                if AplusB(guess6) == 4 and guess6[1][0] != 4:
                    from_4B_to_4A(guess6)
            if AplusB(guess5) == 3:
                from_4B_to_4A(guess1[0][0] + guess1[0][3] + guess2[0][1] + guess2[0][3])
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 1 and AplusB(guess4) == 1:
            from_4B_to_4A(guess1[0][0] + guess1[0][3] + guess2[0][0] + guess2[0][3])


def from_2B_to_3B(guess):
    # Based on the following 1~2 guesses, all 12 groups are formed: 12, 13, 21, 22, 3
    guess3 = hints(pick_x_number_from_not_used(1) + guess[0][0:3])

    if AplusB(guess3) == 3:
        # This is a special return, it returns a length of 3 instead of normal length of 2.
        # It will return 2 incorrect numbers at the 3rd element for later use by from_no_info_3B_to_4A.
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
def from_definite_2B_and_2_to_4A(guess, two_definite_correct_numbers=''):
    # Because there are only 2 correct numbers from first 2 guesses, so the 2 un-guessed numbers must be correct,
    # namely 'two_definite_correct_numbers' as the 2nd variable for this function.

    # If these 2 numbers have been given from from_definite_2B_and_1_to_4A(), then we won't need to pick again.
    if two_definite_correct_numbers is '':
        two_definite_correct_numbers = pick_x_number_from_not_used(2)

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
    # TODO: this guess might be duplicated with the last guess from from_definite_2B_and_1_to_4A().
    guess3 = hints(two_definite_correct_numbers + two_numbers)

    if AplusB(guess3) == 4 and guess3[1][0] != 4:
        from_4B_to_4A(guess3)

    elif AplusB(guess3) == 2:
        from_4B_to_4A((two_definite_correct_numbers + other_two_numbers))

    elif AplusB(guess3) == 3:
        guess4 = hints(two_definite_correct_numbers + one_number + one_number_in_others)
        if AplusB(guess4) == 4 and guess4[1][0] != 4:
            from_4B_to_4A(guess4)
        elif AplusB(guess4) == 2:
            from_4B_to_4A(two_definite_correct_numbers + another_number + another_number_in_others)
        elif AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(two_definite_correct_numbers + one_number + another_number_in_others))
            if AplusB(guess5) == 4 and guess5[1][0] != 4:
                from_4B_to_4A(guess5)
            elif AplusB(guess5) == 2:
                from_4B_to_4A(two_definite_correct_numbers + one_number_in_others + another_number)


# '2B_and_1' means besides the 2 definite correct numbers, the other 2 correct numbers are different 2 guess (1+1).
def from_definite_2B_and_1_to_4A(guess1, guess2):
    two_other_correct_numbers_are_in_this_guess = None

    # Because there are only 2 correct numbers from first 2 guesses, so the 2 un-guessed numbers must be correct.
    two_definite_correct_numbers = pick_x_number_from_not_used(2)

    # These 2 guesses are trying to find the correct numbers from which half.
    # TODO: think about how to use next_best_guess().
    guess_1 = hints(two_definite_correct_numbers + guess1[0][0:2])
    guess_2 = hints(guess2[0][2:4] + two_definite_correct_numbers)

    if AplusB(guess_1) == 3 and AplusB(guess_2) == 3:
        two_other_correct_numbers_are_in_this_guess = guess1[0][0:2] + guess2[0][2:4]
    if AplusB(guess_1) == 3 and AplusB(guess_2) == 2:
        two_other_correct_numbers_are_in_this_guess = guess1[0][0:2] + guess2[0][0:2]
    if AplusB(guess_1) == 2 and AplusB(guess_2) == 3:
        two_other_correct_numbers_are_in_this_guess = guess1[0][2:4] + guess2[0][2:4]
    if AplusB(guess_1) == 2 and AplusB(guess_2) == 2:
        two_other_correct_numbers_are_in_this_guess = guess1[0][2:4] + guess2[0][0:2]

    from_definite_2B_and_2_to_4A((two_other_correct_numbers_are_in_this_guess, [0, 0, 0]), two_definite_correct_numbers)


# "no_info_3B" here means there's no previous guess from which we can deduct at least 2 correct numbers in this 3B.
def from_no_info_3B_to_4A(guess, guess1):
    # This if is to identify the last correct number from 2 numbers (not 4).
    if len(guess1[0]) == 4:
        # two_numbers are from guess1.
        two_numbers = pick_number_from_a_string(guess1[0], 2)
        guess3 = None  # We need a guess3 here to identify the last correct number from 2 numbers (not 4).

        if len(guess) == 2:
            # TODO: think about how to use next_best_guess().
            guess3 = hints(pick_x_number_from_not_used(2) + two_numbers)
        # Below is the use of a special return from from_2B_to_3B, it returns a length of 3 instead 2.
        # The 3rd element contains 2 incorrect numbers.
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

    if AplusB(guess3) == 4 and guess3[1][0] != 4:
        from_4B_to_4A(guess3)

    else:
        guess4 = hints(guess[0][1:4] + another_number)

        if AplusB(guess3) == 2 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess3[0][1:3] + guess4[0][2:4]))
            if AplusB(guess5) != 4:
                from_4B_to_4A(next_best_guess(guess3[0][1] + guess4[0][1:4]))
            elif guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 2 and AplusB(guess4) == 4 and guess4[1][0] != 4:
            from_4B_to_4A(guess4)

        if AplusB(guess3) == 3 and AplusB(guess4) == 2:
            guess5 = hints(next_best_guess(guess3[0][0:2] + guess4[0][1:3]))
            if AplusB(guess5) != 4:
                from_4B_to_4A(next_best_guess(guess3[0][0:3] + guess4[0][2]))
            elif guess5[1][0] != 4:
                from_4B_to_4A(guess5)

        if AplusB(guess3) == 3 and AplusB(guess4) == 3:
            guess5 = hints(next_best_guess(guess3[0][0] + guess4[0][0:3]))
            if AplusB(guess5) != 4:
                from_4B_to_4A(next_best_guess(guess4[0][3] + guess3[0][1:4]))
            elif guess5[1][0] != 4:
                from_4B_to_4A(guess5)


# This is the normal version of 3B_to_4A.
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
        # TODO: The current next_best_guess() design will guarantee to return non-empty list, so temp cannot be None.
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            guess7 = hints(next_best_guess(guess[0][0:3] + another_number_in_others))
            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                from_4B_to_4A(guess7)
            if AplusB(guess7) == 2:
                from_4B_to_4A(guess[0][1:4] + one_number_in_others)
        else:
            guess7 = hints(temp)

            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                from_4B_to_4A(guess7)

            if AplusB(guess7) == 3:
                guess8 = hints(next_best_guess(guess[0][0:3] + another_number_in_others))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    from_4B_to_4A(guess8)
                if AplusB(guess8) == 2:
                    from_4B_to_4A((guess[0][1:4] + one_number_in_others))

            if AplusB(guess7) == 2:
                guess8 = hints(next_best_guess(guess[0][1:4] + another_number_in_others))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    from_4B_to_4A(guess8)

    if AplusB(guess6) == 3:
        temp = next_best_guess(guess[0][0:3] + one_number)
        # TODO: The current next_best_guess() design will guarantee to return non-empty list, so temp cannot be None.
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            guess7 = hints(next_best_guess(guess[0][0:3] + another_number))
            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                from_4B_to_4A(guess7)
            if AplusB(guess7) == 2:
                from_4B_to_4A(guess[0][1:4] + one_number)
        else:
            guess7 = hints(temp)

            if AplusB(guess7) == 4 and guess7[1][0] != 4:
                from_4B_to_4A(guess7)

            if AplusB(guess7) == 3:
                guess8 = hints(next_best_guess(guess[0][0:3] + another_number))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    from_4B_to_4A(guess8)
                if AplusB(guess8) == 2:
                    from_4B_to_4A((guess[0][1:4] + one_number))

            if AplusB(guess7) == 2:
                guess8 = hints(next_best_guess(guess[0][1:4] + another_number))
                if AplusB(guess8) == 4 and guess8[1][0] != 4:
                    from_4B_to_4A(guess8)


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
        # TODO: The current next_best_guess() design will guarantee to return non-empty list, so temp cannot be None.
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            hints(next_best_guess(three + another_number_in_others))
        else:
            guess6 = hints(next_best_guess(temp))
            if AplusB(guess6) == 3:
                from_4B_to_4A(three + another_number_in_others)
            if AplusB(guess6) == 4 and guess6[1][0] != 4:
                from_4B_to_4A(guess6)

    if AplusB(guess5) == 3:
        temp = next_best_guess(three + one_number)
        # TODO: The current next_best_guess() design will guarantee to return non-empty list, so temp cannot be None.
        if temp is None:  # Because there is no valid guess for temp, so we move onto make next available guess.
            hints(next_best_guess(three + another_number))
        else:
            guess6 = hints(next_best_guess(temp))
            if AplusB(guess6) == 3:
                from_4B_to_4A(three + another_number)
            if AplusB(guess6) == 4 and guess6[1][0] != 4:
                from_4B_to_4A(guess6)


'''******************************************************************************************************************'''


def play():
    # Based on the first 1~2 guesses, all 12 groups are: 02, 03, 04, 11, 12, 13, 20, 21, 22, 30, 31, 4
    guess1 = hints(gen_number(4))
    # For testing purpose:
    # guess1 = hints('1234')

    # Similar algorithm for group 4 & 04 ---------------------------------------
    if AplusB(guess1) == 4:
        if guess1[1][0] != 4:
            from_no_info_4B_to_4A()
    else:
        guess2 = hints(pick_x_number_from_not_used(4))
        # For testing purpose:
        # guess2 = hints('5678')

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
            elif len(info) == 4 and three_b[1][0] != -1:  # This '-1' is a flag, please refer to from_2B_to_3B().
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

        # Lonely group 22 ---------------------------------------
        if AplusB(guess1) == 2 and AplusB(guess2) == 2:
            from_2B_to_4A(guess1, guess2)


# This is the demo to show how a normal game processes.
def play_one_game():
    global number
    number = gen_number(4)
    print 'Target number: ' + str(number)
    play()
    print 'Xth:   guess:  hint:'
    for i in range(1, 12):
        for j in info:
            if info[j][2] == i:
                print str(i) + '      ' + str(j) + '    ' + str(info[j][0]) + 'A' + str(info[j][1]) + 'B'


# This is for testing, the loop will break if condition set satisfied.
def play_one_hundred_game():
    # Timer.
    start_time = time.time()

    global number, success, ten_numbers, info, counter
    # The 0th element is total steps, the ith element is the count of games that completes within that step.
    steps = [0 * i for i in range(0, 15)]
    for i in range(0, 100):
        number = gen_number(4)
        print number
        play()
        print info

        # Do statistics.
        steps[0] += counter - 1
        for j in range(1, 15):
            if counter == j:
                steps[j] += 1

        # For testing purpose.
        if counter >= 100:
            break

        # Reset variables after each game.
        ten_numbers = '0123456789'
        info = {}
        counter = 0

    # Timer.
    end_time = time.time()

    # Output.
    print 'Statistics:'
    print 'Game played: 100'
    print 'Successes: ' + str(success)
    print 'Failures: ' + str(100 - success)
    print 'Time used: ' + str(round(end_time - start_time, 2)) + ' seconds'
    print 'Total steps: ' + str(steps[0])
    print 'Average steps: ' + str(round(float(steps[0]) / float(100), 2))
    print 'How many games completed with that steps:'
    for i in range(1, 15):
        print str(i) + ' steps: ' + str(steps[i])


# This is for statistics.
def play_one_hundred_thousand_game():
    # Timer.
    start_time = time.time()

    global number, success, ten_numbers, info, counter
    # The 0th element is total steps, the ith element is the count of games that completes within that step.
    steps = [0 * i for i in range(0, 15)]
    for i in range(0, 100000):
        number = gen_number(4)
        print number
        play()
        print info

        # Do statistics.
        steps[0] += counter
        for j in range(1, 15):
            if counter == j:
                steps[j] += 1

        # Reset variables after each game.
        ten_numbers = '0123456789'
        info = {}
        counter = 0

    # Timer.
    end_time = time.time()

    # Output.
    print 'Statistics:'
    print 'Game played: 100000'
    print 'Successes: ' + str(success)
    print 'Failures: ' + str(100000 - success)
    print 'Time used: ' + str(round(end_time - start_time, 2)) + ' seconds'
    print 'Total steps: ' + str(steps[0])
    print 'Average steps: ' + str(round(float(steps[0]) / float(100000), 2))
    print 'How many games completed with that steps:'
    for i in range(1, 15):
        print str(i) + ' steps: ' + str(steps[i])


if __name__ == '__main__':
    play_one_game()
    # play_one_hundred_game()
    # play_one_hundred_thousand_game()
