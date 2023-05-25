from random import choices


class Organism:

    def __init__(self, length, genome=None):
        self._genome = choices(range(1, 11), k=length)
        self._color = (sum(self._genome)*4+50, 100, 150)

    def __str__(self) -> str:
        return str(self._genome)