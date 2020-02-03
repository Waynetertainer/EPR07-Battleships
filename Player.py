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
        self.placement_frame = tk.Frame(root)
        self.shooting_frame = tk.Frame(root)
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

    def print_board(self, parent):
        """Displays the board.

        offset describes how many rows are skipped before the board is
        displayed. This allows multiple boards to be displayed on top of
        each other.
        If hidden is true, ships not hit will be disguised.
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                pass
                # if hidden:
                #     if self.board[row][column][1] == "ship":
                #         self.board[row][column][0]["text"] = Player.symbols["water"]
        self.board_frame.grid()
        # TODO: button has to move, print has to be universal
        # TODO: add confirm_placement function

    def show_placing(self):
        """Displays the board in placement mode."""
        add_ship_button = tk.Button(self.placement_frame, text=("Schiff hinzufügen"), command=self.add_ship)
        add_ship_button.grid(columnspan=6)
        # self.board_frame["parent"] = self.placement_frame
        self.placement_frame.grid()
        self.board_frame.grid()
        # self.print_board(self.placement_frame)
        confirm_placement_button = tk.Button(self.board_frame, text=("Platzierung bestätigen"), command=lambda: self.board_frame.grid_forget())
        confirm_placement_button.grid(columnspan=6)

    def show(self):
        """Displays the board in shooting mode."""
