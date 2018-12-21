#!/usr/bin/env python

import sys
import random

SLOTS = 4
RANGE = 10


class Result:
    A = -1
    B = -1

    def __init__(self, a, b):
        self.A = a
        self.B = b

    def __str__(self):
        return str(self.A) + "A" + str(self.B) + "B"

    def __eq__(self, other):
        if self.A == other.A and self.B == other.B:
            return True
        return False


class Guess:

    def __init__(self):
        self._array = []
        for i in xrange(SLOTS):
            self._array.append(0)
        # self.reset()

    def _next(self):
        i = 0
        has_next = True
        while has_next:
            self._array[i] = self._array[i] + 1
            has_next = False
            if self._array[i] == RANGE:
                self._array[i] = 0
                has_next = True
            i += 1

    def next_valid(self):
        self._next()
        while not self.is_valid() and not self.is_max():
            self._next()

    def is_valid(self):
        for i in xrange(SLOTS):
            for j in xrange(SLOTS):
                if i == j:
                    continue
                if self._array[i] == self._array[j]:
                    return False
        return True

    def is_max(self):
        for i in xrange(SLOTS):
            if self._array[i] != RANGE - 1:
                return False
        return True

    # def print_it(self):
    #     for i in xrange(SLOTS):
    #         sys.stdout.write(str(self._array[i]) + ' ')
    #     print

    def get_result(self, guess):
        a = 0
        b = 0
        for i in xrange(SLOTS):
            if guess[i] == self._array[i]:
                a += 1
            else:
                for j in xrange(SLOTS):
                    if j == i:
                        continue
                    else:
                        if guess[i] == self._array[j]:
                            b += 1
                            break
        return Result(a, b)

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        self._array[key] = value

    def __eq__(self, other):
        for i in xrange(SLOTS):
            if self._array[i] != other[i]:
                return False
        return True

    def __str__(self):
        return str(self._array)


class Puzzle:
    def __init__(self):
        self._isSolved = False
        self._answer = Guess()
        while not self._answer.is_valid():
            for i in xrange(SLOTS):
                self._answer[i] = random.randint(0, RANGE - 1)

    def is_solved(self):
        return self._isSolved

    def get_answer(self):
        return self._answer

    def guess(self, guess):  # Result
        if not guess.is_valid():
            print "!!! guess not valid!"
            return Result(-1, -1)

        ret = self._answer.get_result(guess)
        if ret.A == SLOTS and ret.B == 0:
            self._isSolved = True
        return ret


class MyPuzzleSolver:
    # public:
    def __init__(self):
        self._last = None
        self._guess_times = 0
        self._guess_set = []
        self._times = []
        self.init()

    def get_guess_times(self):
        return self._guess_times

    def show_matrix(self):
        print '------------- possibility matrix ----------------'
        for i in xrange(SLOTS):
            for j in xrange(RANGE):
                sys.stdout.write(str(self._times[i][j]) + " ")
            print
        print '-------------------------------------------------'

    def show_possibility(self):
        print '------------- possibility guess ----------------'
        for i in xrange(len(self._guess_set)):
            self._guess_set[i].print_it()
        print '------------- total: %s possibility ------------' % len(self._guess_set)

    def init(self):
        for i in xrange(SLOTS):
            new = []
            for j in xrange(RANGE):
                new.append(0)
            self._times.append(new)

        # print self._times
        temp_guess = Guess()
        while not temp_guess.is_max():
            self.add_possibility(temp_guess)
            temp_guess.next_valid()
            # temp_guess.print_it()
        # print len(self._guess_set)

    def add_possibility(self, guess):
        if not guess.is_valid():
            return
        for i in xrange(SLOTS):
            self._times[i][guess[i]] += 1

        # clone a new obj
        new_guess = Guess()
        for i in xrange(SLOTS):
            new_guess[i] = guess[i]

        self._guess_set.append(new_guess)

    def remove_possibility(self, guess):
        if not guess.is_valid():
            return
        for i in xrange(SLOTS):
            self._times[i][guess[i]] -= 1
        self._guess_set.remove(guess)

    def next_guess(self):
        self._guess_times += 1
        self._last = self._guess_set[0]
        if self._guess_times == 1:
            return self._last

        total_times = 1
        for poss_guess in self._guess_set:
            times_of_current = 1
            for i in xrange(SLOTS):
                times_of_current *= self._times[i][poss_guess[i]]
            # find the most possible guess
            if times_of_current > total_times:
                total_times = times_of_current
                self._last = poss_guess
        return self._last

    def remove_possibility_base_on_my_guess(self, my_guess, result):
        to_be_removed = []
        for guess in self._guess_set:
            if not guess.get_result(my_guess) == result:
                to_be_removed.append(guess)

        for to_be_removed_guess in to_be_removed:
            self.remove_possibility(to_be_removed_guess)


def play():
    puzzle = Puzzle()
    ai = MyPuzzleSolver()

    while not puzzle.is_solved():
        # TODO uncomment below lines to show more output
        # solver.show_matrix()
        # solver.show_possibility()
        my_guess = ai.next_guess()
        my_result = puzzle.guess(my_guess)
        ai.remove_possibility_base_on_my_guess(my_guess, my_result)
        print my_guess
        print my_result

    times = ai.get_guess_times()
    print "with %s steps in this game" % times
    return times


def statistic(times):
    guesses = 0
    count = 0
    for i in xrange(times):
        guesses += play()
        count += 1
        print "%s games, %.2f guesses each game in average." % (count, guesses * 1.0 / count)


TOTAL_TIMES = 1000
if __name__ == '__main__':
    statistic(TOTAL_TIMES)
