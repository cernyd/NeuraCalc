import abc
from math import floor, log10
from random import choice, randint, random
from time import time


def nearest_upper(num):
    return 10**(floor(log10(num))+1)


class Exercise(abc.ABC):
    def __init__(self):
        self.duration = 0
        self.answer_correct = False
        self.user_answer = None

    @abc.abstractproperty
    def correct_answer(self):
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
            self.user_answer = int(answer)
            self.answer_correct = self.user_answer == self.correct_answer
            self.duration = time() - self.duration
            return self.answer_correct
        except ValueError:
            raise ValueError("Please enter a number!")


class MulBy11(NumericExercise):
    def __init__(self, start=10, end=99):
        super().__init__()

        self._x = randint(start, end)

    @property
    def correct_answer(self):
        return self._x * 11

    @property
    def _prompt(self):
        if random() < 0.5:
            return f"{self._x} x 11 = ?"
        else:
            return f"11 x {self._x} = ?"

    @property
    def solution(self):
        return f"{self._x} x 11 = {self.correct_answer}"


class TwoDigitSquare(NumericExercise):
    def __init__(self):
        super().__init__()

        self._x = randint(1, 9) * 10 + 5

    @property
    def correct_answer(self):
        return self._x**2

    @property
    def _prompt(self):
        return f"{self._x}^2 = ?"

    @property
    def solution(self):
        return f"{self._x}^2 = {self.correct_answer}"


class ComplementMul(NumericExercise):
    def __init__(self):
        super().__init__()

        digit = randint(1, 9) * 10
        digit2 = randint(1, 9)

        self._x = digit + digit2
        self._y = digit + (10 - digit2)

    @property
    def correct_answer(self):
        return self._x * self._y

    @property
    def _prompt(self):
        return f"{self._x} x {self._y} = ?"

    @property
    def solution(self):
        return f"{self._x} x {self._y} = {self._x * self._y}"


class NumComplement(NumericExercise):
    def __init__(self):
        super().__init__()

        self._exp = randint(1, 3)
        self._x = randint(1*10**self._exp, 9*10**self._exp)
        self._nearest = nearest_upper(self._x)

    @property
    def correct_answer(self):
        return self._nearest - self._x

    @property
    def _prompt(self):
        return f"Complement of {self._x} = ?"

    @property
    def solution(self):
        return f"Complement of {self._x} = {self.correct_answer}"


class AdditionExercise(NumericExercise):
    def __init__(self, max_digits=3):
        super().__init__()

        a_digits = randint(2, max_digits)
        b_digits = randint(2, a_digits)
        self._a = randint(10**a_digits, 9*10**a_digits)
        self._b = randint(10**b_digits, 9*10**b_digits)

    @property
    def correct_answer(self):
        return self._a + self._b

    @property
    def _prompt(self):
        if random() < 0.5:
            return f"{self._a} + {self._b} = ?"
        else:
            return f"{self._b} + {self._a} = ?"

    @property
    def solution(self):
        return f"{self._a} + {self._b} = {self.correct_answer}"


class SubtractionExercise(NumericExercise):
    def __init__(self, max_digits=3):
        super().__init__()

        a_digits = randint(2, max_digits)
        b_digits = randint(2, a_digits)
        self._a = randint(10**a_digits, 9*10**a_digits)

        b_max = 90**b_digits
        if a_digits == b_digits:
            b_max = self._a

        self._b = randint(10**b_digits, b_max)

    @property
    def correct_answer(self):
        return self._a - self._b

    @property
    def _prompt(self):
        return f"{self._a} - {self._b} = ?"

    @property
    def solution(self):
        return f"{self._a} - {self._b} = {self.correct_answer}"


EXERCISES = (
    MulBy11, TwoDigitSquare, ComplementMul, NumComplement,
    AdditionExercise, SubtractionExercise
)


class ExerciseGenerator:
    def __init__(self, count=25):
        self.answers = {}
        self.count = count
        self.i = 0

        for e in EXERCISES:
            self.answers[e.__name__] = []

    @property
    def results(self):
        return self.answers

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.count:
            raise StopIteration()

        self.i += 1

        e = choice(EXERCISES)()
        self.answers[e.__class__.__name__].append(e)
        return e
