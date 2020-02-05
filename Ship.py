"""Provides the Ship class."""

# header


class Ship:
    """A ship with its own hitpoints."""

    def __init__(self):
        """Initializes a Ship."""
        self.fields = {}

    def sunk(self):
        """Return whether all field of the shit are hit."""
        return all(hit for hit in self.fields.values())

    def hit_field(self, y, x):
        """Marks a field as hit."""
        self.fields.update({(y, x): True})

    def add_field(self, y, x):
        """Adds a field to the Ship."""
        self.fields.update({(y, x): False})

    def remove_field(self, y, x):
        """Removes a field from the ship."""
        # Try to remove a field that is'n even in the ship.
        if (y, x) not in self.fields.keys():
            print("FATAL ERROR")
            return False
        # Check every field around the given position.
        adjacent_counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # The given field doesn't count against the number of adjacent
                # fields.
                if not j == i == 0:
                    if (y + i, x + j) in self.fields.keys():
                        adjacent_counter += 1
        # If there is no or only one field around the given position, the
        # given field is and end of the ship and can be deleted. Otherwise
        # the field is in the middle of the ship and can not be deleted.
        if adjacent_counter <= 1:
            del self.fields[(y, x)]
            return True
        else:
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
        elif list(self.fields.keys())[0][0] == list(self.fields.keys())[1][0]:
            for field in self.fields.keys():
                if y == field[0] and (x == field[1] - 1 or x == field[1] + 1):
                    return True
        elif list(self.fields.keys())[0][1] == list(self.fields.keys())[1][1]:
            for field in self.fields.keys():
                if x == field[1] and (y == field[0] - 1 or y == field[0] + 1):
                    return True
        return False
