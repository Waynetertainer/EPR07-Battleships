"""Provides the Ship class."""

# header


class Ship:
    """A ship with its own hitpoints."""

    def __init__(self):
        """Initializes a Ship."""
        self.fields = {}

    def add_field(self, y, x):
        """Adds a field to the Ship."""
        self.fields.update({(y, x): False})

    def remove_field(self, y, x):
        """Removes a field from the ship."""
        if (y, x) not in self.fields.keys():
            print("ERROR")
            return False
        for field in self.fields.keys():
            if len(self.fields) == 1:
                del self.fields[(y, x)]
                return True
            if (y + 1, x) not in self.fields.keys() and (y - 1, x) in self.fields.keys():
                del self.fields[(y, x)]
                return True
            if (y - 1, x) not in self.fields.keys() and (y + 1, x) in self.fields.keys():
                del self.fields[(y, x)]
                return True
            if (y, x + 1) not in self.fields.keys() and (y, x + 1) in self.fields.keys():
                del self.fields[(y, x)]
                return True
            if (y, x - 1) not in self.fields.keys() and (y, x - 1) in self.fields.keys():
                del self.fields[(y, x)]
                return True
            return False


    def is_next_to(self, y, x):
        """Checks whether a position is adjacent to the ship."""
        if len(self.fields) == 0:
            return True

        if len(self.fields) == 1:
            for field in self.fields.keys():
                if y == field[0]:
                    if x == field[1] + 1 or x == field[1] - 1:
                        return True
                elif x == field[1]:
                    if y == field[0] + 1 or y == field[0] - 1:
                        return True
        elif self.fields.keys()[0][0] == self.fields.keys()[1][0]:
            for field in self.fields.keys():
                pass
                #TODO continue working
                #nur wenn das schiff in reihe ist...

        return False
