import abc
from math import floor, log10
from random import choice, randint, random
from time import time


def nearest_upper(num):
    return 10**(floor(log10(num))+1)


class Exercise(abc.ABC):
    def __init__(self):
        self.duration = -1
        self.answer_correct = False

    @abc.abstractproperty
    def answer(self):
        return None

    @abc.abstractmethod
    def check_answer(self, answer):
        return False

    @abc.abstractproperty
    def _prompt(self):
        return None

    @property
    def prompt(self):
        self.duration = time()
        return self._prompt

    @abc.abstractproperty
    def solution(self):
        return "SOLUTION"

    def hint(self):
        return None


class NumericExercise(Exercise):
    def check_answer(self, answer):
        try:
            self.answer_correct = int(answer) == self.answer
            self.duration = time() - self.duration
            return self.answer_correct
        except ValueError:
            raise ValueError("Please enter a number!")


class MulBy11(NumericExercise):
    def __init__(self, start=10, end=99):
        self._x = randint(start, end)

    @property
    def answer(self):
        return self._x * 11

    @property
    def _prompt(self):
        if random() < 0.5:
            return f"{self._x} x 11 = ?"
        else:
            return f"11 x {self._x} = ?"

    @property
    def solution(self):
        return f"{self._x} x 11 = {self.answer}"


class TwoDigitSquare(NumericExercise):
    def __init__(self):
        self._x = randint(1, 9) * 10 + 5

    @property
    def answer(self):
        return self._x**2

    @property
    def _prompt(self):
        return f"{self._x}^2 = ?"

    @property
    def solution(self):
        return f"{self._x}^2 = {self.answer}"


class ComplementMul(NumericExercise):
    def __init__(self):
        digit = randint(1, 9) * 10
        digit2 = randint(1, 9)

        self._x = digit + digit2
        self._y = digit + (10 - digit2)

    @property
    def answer(self):
        return self._x * self._y

    @property
    def _prompt(self):
        return f"{self._x} x {self._y} = ?"

    @property
    def solution(self):
        return f"{self._x} x {self._y} = {self._x * self._y}"


class NumComplement(NumericExercise):
    def __init__(self):
        self._exp = randint(1, 3)
        self._x = randint(1*10**self._exp, 9*10**self._exp)
        self._nearest = nearest_upper(self._x)

    @property
    def answer(self):
        return self._nearest - self._x

    @property
    def _prompt(self):
        return f"Complement of {self._x} = ?"

    @property
    def solution(self):
        return f"Complement of {self._x} = {self.answer}"


EXERCISES = (MulBy11, TwoDigitSquare, ComplementMul, NumComplement)


class ExerciseGenerator:
    def __init__(self, reps=5, sets=5):
        self.answers = {}
        self.reps = reps
        self.sets = sets

        self.curr_set = 0
        self.curr_rep = 0

        for e in EXERCISES:
            self.answers[e.__name__] = []

        print(self.answers)

    def results(self):
        print("=== RESULTS ===")
        # print(self.answers)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_rep >= self.reps:
            self.curr_set += 1
            self.curr_rep = 0

        if self.curr_set >= self.sets:
            self.results()
            raise StopIteration()

        self.curr_rep += 1

        e = choice(EXERCISES)()
        self.answers[e.__class__.__name__].append(e)
        return e
