"""Provides the Player class."""

# header

import tkinter as tk
from Ship import Ship


class Player:
    """A Player with name and Board."""

    symbols = {"ship": chr(9744), "water": chr(9781), "ship_hit": chr(9746),
               "water_hit": chr(10060)}

    def shoot(self, y, x):
        """"""
        for i in self.board[0]:
            print(id(i))
        print(y, x)

    def place(self, y, x,):
        """"""
        field = self.board[y][x]
        if field[2] == self.active_ship:
            if self.active_ship.remove_field(y, x):
                self.board[y][x][0]["text"] = Player.symbols["water"]
                self.board[y][x][1] = "water"
                field[2] = None
            else:
                print("Kann nur Anfang und Ende entfernen.")
            return
        if field[2] is not None:
            print("Anderes Schiff ist im Weg.")
            return
        if not self.active_ship.is_next_to(y, x):
            print("Schiffblöcke nur nebeneinander.")
            return
        if len(self.active_ship.fields) >= 6:
            print("Schiff zu lang.")
            return
        self.board[y][x][0]["text"] = Player.symbols["ship"]
        self.board[y][x][1] = "ship"
        self.board[y][x][2] = self.active_ship
        self.active_ship.add_field(y, x)

    def add_ship(self):
        """Confirms the placement of the active ship."""
        if len(self.active_ship.fields) <= 2:
            print("Schiff zu kurz")
        else:
            self.ships.append(self.active_ship)
            self.active_ship = Ship()

    def __init__(self, name, size, root):
        """Initializes a Player."""
        self.board_frame = tk.Frame(root)
        self.active_ship = Ship()
        self.ships = []
        self.name = name
        self.board = list()
        # board is a list of lists of tuples.
        # Each tuple has a Button, a state and maybe a reference to a ship.
        for row in range(size[0]):
            self.board.append([])
            for column in range(size[1]):
                button = tk.Button(self.board_frame,
                                   text=Player.symbols["water"],
                                   command=lambda i=row, j=column:
                                   self.place(i, j))
                button.grid(row=row + 1, column=column + 1)
                field = list((button, "water", None))
                self.board[row].append(field)
                # self.board[row][column][0].grid(row=row + 1, column=column + 1)
                # print(id(self.board[row][column]))
            #     self.board[row][column][0]["command"] = lambda: self.shoot(row, column)
            #     self.board[row][column][0].grid(row=row + 1, column=column + 1)
        # for row in range(size[0]):
        #     self.board.append([])
        #     self.board[row].extend([(tk.Button(self.board_frame, text=Player.symbols["water"], command=lambda: self.shoot(row, i)), "water", None) for i in range(size[1])])
        #     for column in range(size[1]):
        #         # button = tk.Button(self.board_frame, text=Player.symbols["water"], command=lambda: self.shoot(row, column))
        #         # tupel = tuple([button, "water", None, row, column])
        #         # self.board[row].append(tupel)
        #         self.board[row][column][0].grid(row=row + 1, column=column + 1)

        # for i in range(len(self.board)):
        #     print('{:>2}'.format(i + 1), end=" ")
        #     for j in self.board[i]:
        #         print('{:>2}'.format("X"), end="")
        #     print("")

    def print_board(self, offset=0, hidden=True):
        """Displays the board.

        offset describes how many rows are skipped before the board is
        displayed. This allows multiple boards to be displayed on top of
        each other.
        If hidden is true, ships not hit will be disguised.
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if hidden:
                    if self.board[row][column][1] == "ship":
                        self.board[row][column][0]["text"] = Player.symbols["water"]
        self.board_frame.grid(row=offset)
        button = tk.Button(self.board_frame, text=("Schiff hinzufügen"), command=self.add_ship)
        button.grid(columnspan=6)
