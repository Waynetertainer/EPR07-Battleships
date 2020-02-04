"""Provides the Player class."""

# header

import tkinter as tk
import tkinter.messagebox as msg
from Ship import Ship


class Player:
    """A Player with name and Board."""

    symbols = {"ship": chr(9744), "water": chr(9781), "ship_hit": chr(9746),
               "water_hit": chr(10060)}

    def defeated(self):
        """Checks whether a player is defeated."""
        return all(ship.sunk() for ship in self.ships)

    def shoot(self, y, x):
        """Shoots at a given position on the board."""
        field = self.board[y][x]
        if field[1] == "water_hit":
            if tk.messagebox.askokcancel(title="Achtung!",
                                         message="Diese Position wurde bereits beschossen.\
                                          Wollen sie erneut auf diese Stelle schießen?"):
                # TODO implement
                # miss, end turn -> end of turn screen -> gm.nextshoot()
                pass
        elif field[1] == "ship_hit":
            # Nothing happens, even if the player shoots the ship again.
            tk.messagebox.askokcancel(title="Achtung!",
                                         message="Diese Position wurde bereits beschossen.\
                                          Wollen sie erneut auf diese Stelle schießen?")
        elif field[1] == "water":
            field[0].configure(text=Player.symbols["water_hit"])
            field[1] = "water_hit"
            # TODO implement
            # miss, end turn -> end of turn screen -> gm.nextshoot()
        elif field[1] == "ship":
            field[0].configure(text=Player.symbols["ship_hit"])
            field[1] = "ship_hit"
            field[2].hit_field(y, x)
            if self.defeated():
                pass
                # TODO implement
                # tell gamemanager and end turn
            else:
                pass
                # do nothin, the attacker continues

        print("shhot", y, x)

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

    def __init__(self, name, size, root, game_manager):
        """Initializes a Player."""
        self.placement_frame = tk.Frame(root)
        self.shooting_frame = tk.Frame(root)
        self.viewing_frame = tk.Frame(root)
        self.board_frame = tk.Frame(root)
        self.active_ship = Ship()
        self.ships = []
        self.name = name
        self.game_manager = game_manager
        self.board = list()
        # board is a list of lists of tuples.
        # Each tuple has a Button, a state and maybe a reference to a ship.
        for column in range(size[1]):
            tk.Label(self.board_frame, text=chr(column + 65)).grid(row=0, column=column + 1)
        for row in range(size[0]):
            tk.Label(self.board_frame, text=str(row + 1)).grid(row=row + 1, column=0)
            self.board.append([])
            for column in range(size[1]):
                button = tk.Button(self.board_frame,
                                   text=Player.symbols["water"],
                                   command=lambda i=row, j=column:
                                   self.place(i, j))
                button.grid(row=row + 1, column=column + 1)
                field = list((button, "water", None))
                self.board[row].append(field)

    def get_percentage(self):
        """Calculates how much percent of the board is covered."""
        counter = 0
        for row in self.board:
            for field in row:
                if field[2] is not None:  # field[2] holds the ship object.
                    counter += 1
        return counter / (len(self.board) * len(self.board[0]))

    def place_random(self):
        """Fills the board randomly."""
        if len(self.ships) < 1:
            print("Mindestens ein Schiff muss zuvor platziert worden sein.")
        else:
            # TODO implement
            pass
        print("Fill random")

    def reset_board(self):
        """Resets the board to default values."""
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                self.board[row][column][0].configure(text=Player.symbols["water"],
                                                     command=lambda i=row, j=column:
                                                     self.place(i, j))
                self.board[row][column][1] = "water"
                self.board[row][column][2] = None
        self.ships = list()

    def print_board(self, hidden):
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
        self.board_frame.grid(column=0, columnspan=len(self.board[0]) + 1)

    def show_placing(self, game_manager):
        """Displays the board in placement mode."""

        def end_placement():
            """Ends placement and closes all frames."""
            if 0.1 <= self.get_percentage() <= 0.25 and len(self.ships) >= 2:
                self.board_frame.grid_forget()
                self.placement_frame.grid_forget()
                game_manager.next_placement()
            else:
                print("Anzahl der Schiffe nicht zulässig.")

        tk.Label(self.placement_frame, text=self.name + ", bitte platziere deine Schiffe").grid(row=0, column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for deleting all ships.
        delete_ships_button = tk.Button(self.placement_frame, text=("Alle Schiffe löschen"), command=self.reset_board)
        delete_ships_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for confirming placement of one ship.
        add_ship_button = tk.Button(self.placement_frame, text=("Aktuelles Schiff bestätigen"), command=self.add_ship)
        add_ship_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for filling the board randomly.
        fill_random_button = tk.Button(self.placement_frame, text=("Zufällig platzieren"), command=self.place_random)
        fill_random_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for confirming the final placement of all ships.
        confirm_placement_button = tk.Button(self.placement_frame, text=("Platzierung bestätigen"), command=end_placement)
        confirm_placement_button.grid(column=0, columnspan=self.board_frame.size()[1] + 3,  sticky="WE")
        self.placement_frame.grid()
        self.print_board(False)

    def show_shooting(self):
        """Displays the board in shooting mode."""
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                self.board[row][column][0].configure(text=Player.symbols["water"],
                                                     command=lambda i=row, j=column:
                                                     self.shoot(i, j))
        tk.Label(self.shooting_frame, text=self.name + "'s Spielfeld").grid(columnspan=self.board_frame.size()[1], sticky="WE")
        self.shooting_frame.grid()
        self.print_board(True)

    def show_viewing(self):
        """Displays the board without any functionality."""
        for row in self.board:
            for field in row:
                field[0].configure(command=lambda: ())
                field[0].configure(text="A")
        tk.Label(self.viewing_frame, text="Eigenes Spielfeld").grid(columnspan=self.board_frame.size()[1], sticky="WE")
        self.viewing_frame.grid()
        self.print_board(False)
