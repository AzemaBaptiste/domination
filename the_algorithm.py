"""
Print numbers from 1 to LEET (1337)
replace the number by "Sha" if it's a multiple of 3
replace the number by "Dow" if it's a multiple of 5
replace the number by "ShaDow" if it's a multiple of 3 and 5
"""


class TheAlgorithm:
    """
    Main class running TheAlgorithm
    """

    def __init__(self, limit: int):
        self.limit: int = limit

    @staticmethod
    def evaluate(number: int) -> str:
        if number % 15 == 0:
            return 'ShaDow'
        if number % 3 == 0:
            return 'Sha'
        if number % 5 == 0:
            return 'Dow'
        return str(number)

    def worker(self, i: int) -> str:
        evaluate = self.evaluate(i)
        print(evaluate)
        return evaluate

    def generator(self):
        for i in range(1, self.limit + 1):
            self.worker(i)


def main(limit: int):
    TheAlgorithm(limit).generator()


if __name__ == '__main__':
    main(1337)
