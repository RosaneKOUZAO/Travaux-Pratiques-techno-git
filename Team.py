from abc import ABC, abstractmethod
import TeamIterator

class Team(ABC):
    def __init__(self, members):
        self._members = members  

    def __len__(self):
        return len(self._members)

    def __getitem__(self, index):
        return self._members[index]

    def __iter__(self):
        return TeamIterator(self._members)
