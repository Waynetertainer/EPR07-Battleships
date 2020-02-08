"""Provides the Player class."""

__author__ = "6601128, Schademan, 7232927, Tobias"
__credits__ = ""
__email__ = "schejda@googlemail.com, s0798915@rz.uni-frankfurt.de"

import tkinter as tk
import tkinter.messagebox
import random as rnd
import time
from Ship import Ship


class Player:
    """A Player with name and Board."""

    symbols = {"ship": chr(9744), "water": chr(9781), "ship_hit": chr(9746),
               "water_hit": chr(10060)}

    def defeated(self):
        """Checks whether a player is defeated."""
        return all(ship.sunk() for ship in self.ships)

    def shoot(self, y, x, spray=False):
        """Shoots at a given position on the board."""
        if spray:
            # 50% Chance of spraying.
            if rnd.random() >= 0.5:
                possible_fields = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= y + i < len(self.board):
                            if 0 <= x + j < len(self.board[0]):
                                # possible_fields will contain every valid
                                # position around the given position.
                                possible_fields.append((y + i, x + j))
                if len(possible_fields) == 0:
                    raise Exception("Field error.")
                else:
                    # Select a random field from the possible fields.
                    target_position = rnd.choice(possible_fields)
                    # Shoot at the new field (with spray=False)
                    self.shoot(target_position[0], target_position[1])
                return

        self.opponent.shots -= 1
        self.opponent.shots_label["text"] = self.opponent.shots
        field = self.board[y][x]
        if field[1] == "water_hit":
            if tk.messagebox.askokcancel(title="Achtung!",
                                         message="Diese Position wurde bereits beschossen.\
                                          Wollen sie erneut auf diese Stelle schießen?"):
                if self.game_manager.options["shot_per_ship"]:
                    if self.opponent.shots == 0:
                        self.clear()
                        self.game_manager.no_shots_left()
                else:
                    self.clear()
                    self.game_manager.miss()
        elif field[1] == "ship_hit":
            # Nothing happens, even if the player shoots the ship again.
            # Only the amount of shots is reduced.
            if tk.messagebox.askokcancel(title="Achtung!",
                                         message="Diese Position wurde bereits beschossen.\
                                          Wollen sie erneut auf diese Stelle schießen?"):
                if self.game_manager.options["shot_per_ship"]:
                    if self.opponent.shots == 0:
                        self.clear()
                        self.game_manager.no_shots_left()
        elif field[1] == "water":
            field[0]["text"] = Player.symbols["water_hit"]
            field[1] = "water_hit"
            if self.game_manager.options["shot_per_ship"]:
                if self.opponent.shots == 0:
                    self.clear()
                    self.game_manager.no_shots_left()
            else:
                self.clear()
                self.game_manager.miss()
        elif field[1] == "ship":
            field[0]["text"] = Player.symbols["ship_hit"]
            field[1] = "ship_hit"
            field[2].hit_field(y, x)
            if self.defeated():
                # Remove the player from the list of players.
                self.game_manager.defeat()
            elif self.game_manager.options["shot_per_ship"]:
                if self.opponent.shots == 0:
                    self.clear()
                    self.game_manager.no_shots_left()

    def place(self, y, x):
        """Places one part of a ship."""

        field = self.board[y][x]
        if field[2] == self.active_ship:
            # Clicking on a part of the active ship removes that part.
            # This part must not be in the middle of a ship.
            if self.active_ship.remove_field(y, x):
                self.board[y][x][0]["text"] = Player.symbols["water"]
                self.board[y][x][1] = "water"
                field[2] = None
            else:
                tk.messagebox.showerror(
                    message="Kann Schiffblöcke nur am Anfang und Ende entfernen")
            return
        if field[2] is not None:
            # Cant place a ship on another ship.
            # Possibility of same ship is already checked by the first "if".
            tk.messagebox.showerror(message="Anderes Schiff ist im Weg")
            return
        if not self.active_ship.is_next_to(y, x):
            tk.messagebox.showerror(message="Schiffblöcke nur nebeneinander")
            return
        if len(self.active_ship.fields) >= 6:
            tk.messagebox.showerror(message="Schiff ist zu lang")
            return
        # Implicit "else:". Not needed because the previous "if"s return and
        # this part would not be reached.
        self.board[y][x][0]["text"] = Player.symbols["ship"]
        self.board[y][x][1] = "ship"
        self.board[y][x][2] = self.active_ship
        self.active_ship.add_field(y, x)

    def add_ship(self):
        """Confirms the placement of the active ship."""

        if len(self.active_ship.fields) <= 2:
            tk.messagebox.showerror(message="Schiff ist zu kurz")
        else:
            self.ships.append(self.active_ship)
            self.active_ship = Ship()

    def __init__(self, name, size, root, game_manager):
        """Initializes a Player."""
        self.placement_frame = tk.Frame(root)
        self.shooting_frame = tk.Frame(root)
        self.viewing_frame = tk.Frame(root)
        self.board_frame = tk.Frame(root)
        # Only needed for stopping the timer.
        self.visible = False
        self.shots = 1
        self.active_ship = Ship()
        self.ships = []
        self.name = name
        self.game_manager = game_manager
        self.opponent = None
        # board is a list of lists of tuples.
        self.board = list()
        # Labels only needed when the board is displayed.
        # Not part of the variable "self.board".
        for column in range(size[1]):
            tk.Label(self.board_frame, text=chr(column + 65)).grid(row=0, column=column + 1)
        for row in range(size[0]):
            # Labels only needed when the board is displayed.
            # Not part of the variable "self.board".
            tk.Label(self.board_frame, text=str(row + 1)).grid(row=row + 1, column=0)
            self.board.append([])
            for column in range(size[1]):
                # Each tuple has a Button, a state and a reference to a ship.
                button = tk.Button(self.board_frame,
                                   text=Player.symbols["water"],
                                   command=lambda i=row, j=column:
                                   self.place(i, j))
                button.grid(row=row + 1, column=column + 1)
                field = list((button, "water", None))
                self.board[row].append(field)
        # This will only be visible on the viewing_frame.
        quit_button = tk.Button(self.viewing_frame, text="Aufgeben",
                                command=self.game_manager.quit)
        quit_button.grid(row=2, columnspan=self.board_frame.size()[1], sticky="WE")
        tk.Label(self.viewing_frame,
                 text="Eigenes Spielfeld (" +
                      self.name + ")").grid(row=3, columnspan=self.board_frame.size()[1],
                                            sticky="WE")
        tk.Label(self.shooting_frame, text=self.name + "'s Spielfeld").grid(
            columnspan=self.board_frame.size()[1], sticky="WE")
        # This label is created without text because the text is always updated.
        self.shots_label = tk.Label(self.viewing_frame)

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
            tk.messagebox.showerror(
                message="Mindestens ein Schiff muss zuvor platziert worden sein")
        else:
            while self.get_percentage() < 0.2:
                length = rnd.randint(3, 6)
                horizontal = bool(rnd.randint(0, 1))
                if horizontal:
                    y_pos = rnd.randint(0, len(self.board) - 1)
                    x_pos = rnd.randint(0, len(self.board) - 1 - length)
                    # Check whether the space is free.
                    if all(self.board[y_pos][x_pos + i][1] == "water" for i in range(length)):
                        for i in range(length):
                            self.place(y_pos, x_pos + i)
                        self.add_ship()
                else:
                    y_pos = rnd.randint(0, len(self.board) - 1 - length)
                    x_pos = rnd.randint(0, len(self.board) - 1)
                    # Check whether the space is free.
                    if all(self.board[y_pos + i][x_pos][1] == "water" for i in range(length)):
                        for i in range(length):
                            self.place(y_pos + i, x_pos)
                        self.add_ship()

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

    def clear(self):
        """Hides all Frames from this player."""
        self.board_frame.grid_forget()
        self.placement_frame.grid_forget()
        self.shooting_frame.grid_forget()
        self.viewing_frame.grid_forget()

    def print_board(self, hidden):
        """Displays the board.

        If hidden is true, ships not hit will be disguised.
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column][1] == "ship":
                    if hidden:
                        self.board[row][column][0]["text"] = Player.symbols["water"]
                    else:
                        self.board[row][column][0]["text"] = Player.symbols["ship"]
        self.board_frame.grid(column=0, columnspan=len(self.board[0]) + 1)

    def show_placing(self):
        """Displays the board in placement mode."""

        def end_placement():
            """Ends placement and closes all frames."""
            if 0.1 <= self.get_percentage() <= 0.25 and len(self.ships) >= 2:
                self.board_frame.grid_forget()
                self.placement_frame.grid_forget()
                self.game_manager.next_placement()
            else:
                tk.messagebox.showerror(message="Anzahl der Schiffe nicht zulässig")

        tk.Label(self.placement_frame, text=self.name + ", bitte platziere deine Schiffe").grid(
            row=0, column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for deleting all ships.
        delete_ships_button = tk.Button(self.placement_frame, text="Alle Schiffe löschen",
                                        command=self.reset_board)
        delete_ships_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for confirming placement of one ship.
        add_ship_button = tk.Button(self.placement_frame, text="Aktuelles Schiff bestätigen",
                                    command=self.add_ship)
        add_ship_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for filling the board randomly.
        fill_random_button = tk.Button(self.placement_frame, text="Zufällig platzieren",
                                       command=self.place_random)
        fill_random_button.grid(column=0, columnspan=self.board_frame.size()[1], sticky="WE")
        # Button for confirming the final placement of all ships.
        confirm_placement_button = tk.Button(self.placement_frame, text="Platzierung bestätigen",
                                             command=end_placement)
        confirm_placement_button.grid(column=0, columnspan=self.board_frame.size()[1] + 3,
                                      sticky="WE")
        self.placement_frame.grid()
        self.print_board(False)

    def show_shooting(self, opponent):
        """Displays the board in shooting mode."""

        self.opponent = opponent
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                self.board[row][column][0].configure(
                    command=lambda i=row, j=column:
                    self.shoot(i, j, spray=self.game_manager.options["spray"]))
        self.shooting_frame.grid()
        self.print_board(True)

    def show_viewing(self):
        """Displays the board without any functionality."""

        def show_timer():
            """Displays the time left on the timer."""
            if not self.visible:
                return
            if end - time.time() <= 0:
                self.game_manager.timeout()
                return
            time_label["text"] = "Verbleibende Zeit: " + str(int(end - time.time()))
            # refreshes the timer after 750ms.
            self.viewing_frame.after(750, show_timer)

        if self.game_manager.options["shot_per_ship"]:
            self.shots = 0
            for ship in self.ships:
                if not ship.sunk():
                    self.shots += 1

        end = time.time() + float(self.game_manager.options["time"])
        time_label = tk.Label(self.viewing_frame)
        time_label.grid(row=1)

        # Only display the remaining shots if the mode is activated.
        if self.game_manager.options["shot_per_ship"]:
            self.shots_label.grid(row=0)
        self.shots_label["text"] = self.shots

        self.visible = True
        show_timer()
        # Remove the functionality from the buttons.
        # Otherwise the player could shoot at its own ships.
        for row in self.board:
            for field in row:
                field[0].configure(command=lambda: ())
        self.viewing_frame.grid()
        self.print_board(False)
