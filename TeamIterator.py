class TeamIterator:
    def __init__(self, team):
        self.__team = team
        self.__index = 0

    def __next__(self):
        if self.__index >= len(self.__team):
            raise StopIteration
        element = self.__team[self.__index]
        self.__index += 1
        return element
