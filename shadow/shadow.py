"""
Print numbers from 1 to LEET (1337)
replace the number by "Sha" if it's a multiple of 3
replace the number by "Dow" if it's a multiple of 5
replace the number by "ShaDow" if it's a multiple of 3 and 5
"""


class ShaDow:
    """
    Main class running ShaDow application
    """

    @staticmethod
    def evaluate(i):
        if i % 15 == 0:
            return 'ShaDow'
        if i % 3 == 0:
            return 'Sha'
        if i % 5 == 0:
            return 'Dow'
        return i

    def worker(self, i):
        print(self.evaluate(i))

    def generator(self, limit):
        for i in range(1, limit + 1):
            self.worker(i)


def main(limit):
    return ShaDow().generator(limit)


if __name__ == '__main__':
    main(1337)
