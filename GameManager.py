"""Provides the GameManager class."""

# header

import tkinter as tk
import random as rnd
from Player import Player


class GameManager:
    """Manages the game."""

    instance = None

    def __init__(self):
        """Initializes a GameManager"""
        GameManager.instance = self
        self.active_player = 0
        self.players = []
        self.options = {"size": (10, 10), "shot_per_ship": False,
                        "spray": False, "time": 30}
        self.intro = \
            """bla
bla
intro
bla 
bla"""
        self.root = tk.Tk()
        self.root.geometry("400x800+100+100")
        self.start_frame = tk.Frame(self.root)
        self.start_frame.grid()
        self.placement_frame = tk.Frame(self.root)
        self.shooting_frame = tk.Frame(self.root)
        self.names_frame = tk.Frame(self.root)
        self.open_main_menu()
        self.root.mainloop()

    def open_main_menu(self):
        """Displays the main menu"""
        print("open main menu")
        # TODO options button
        tk.Label(self.start_frame, text=self.intro, justify="left").grid(row=0, column=0)
        tk.Button(self.start_frame, text="Start", command=self.start).grid(row=1, column=0)
        self.start_frame.grid()
        # move start button here
        # move intro here

    def get_active_player(self, offset=0):
        """Return the index of the active player."""
        return (self.active_player + offset) % len(self.players)

    def start(self):
        """"""
        self.start_frame.grid_forget()
        self.names_frame.grid()
        tk.Label(self.names_frame, text="Bitte Namen eingeben").grid(columnspan=3)
        player_name_entries = [(tk.Label(self.names_frame, text="Spieler "),
                               tk.Entry(self.names_frame)),
                               (tk.Label(self.names_frame, text="Spieler "),
                               tk.Entry(self.names_frame))]
        for i in range(len(player_name_entries)):
            player_name_entries[i][0]["text"] += str(i + 1) + ":"
            player_name_entries[i][0].grid(row=i + 2, column=0, columnspan=2, sticky="W")
            player_name_entries[i][1].grid(row=i + 2, column=2)

        def add_player():
            """Adds a player."""
            player_name_entries.append((tk.Label(self.names_frame, text="Spieler " + str(len(player_name_entries) + 1) + ":"), tk.Entry(self.names_frame)))
            player_name_entries[-1][0].grid(row=len(player_name_entries) + 2, column=0, columnspan=2, sticky="W")
            player_name_entries[-1][1].grid(row=len(player_name_entries) + 2, column=2)

        def remove_player():
            """Removes a player."""
            if len(player_name_entries) > 2:
                entry = player_name_entries.pop()
                entry[0].grid_forget()
                entry[1].grid_forget()

        def create_players():
            """Creates all players according to their names."""
            if all(player[1].get() != "" for player in player_name_entries):
                # Converts every name on the list into a player object
                for player in player_name_entries:
                    self.players.append(Player(player[1].get(), (self.options["size"]), self.root, self))
                    self.names_frame.grid_forget()
                # Shuffles players so that it is random who begins.
                # rnd.shuffle(self. players)
                # Begins placement for the first player.
                self.next_placement()
            else:
                print("error")

        # Button for adding a player.
        add = tk.Button(self.names_frame, text="+", command=add_player)
        add.grid(row=1, column=0, sticky="WE")
        # Button for removing a player.
        remove = tk.Button(self.names_frame, text="-", command=remove_player)
        remove.grid(row=1, column=1, sticky="WE")
        # Button for confirming all players.
        go_next = tk.Button(self.names_frame, text="Weiter", command=create_players)
        go_next.grid(row=1, column=2)

    def next_placement(self):
        """Checks whether all players placed their board or who is next"""
        # Every player has placed their ships.
        if all(len(player.ships) > 0 for player in self.players):
            self.next_shooting(first_time=True)
        else:
            self.players[self.get_active_player()].show_placing()
            self.active_player += 1

    def next_shooting(self, defeat=False, quit=False, first_time=False):
        """Starts the turn of the next player."""
        print("next shooting")

        def show_shooting_view():
            """Displays the field of opponent and self."""
            self.shooting_frame.grid_forget()
            next_player_button.grid_forget()
            next_player_label.grid_forget()
            miss_label.grid_forget()
            self.players[self.get_active_player(1)].show_shooting()
            self.players[self.get_active_player()].show_viewing()

        def restart_game():
            """Opens the main menu and resets players."""
            print("restart game")
            winner_confirm.grid_forget()
            winner_label.grid_forget()
            self.shooting_frame.grid_forget()
            self.players = list()
            self.open_main_menu()

        self.shooting_frame.grid()
        next_player_button = tk.Button(self.shooting_frame, text="Bereit", command=show_shooting_view)
        winner_confirm = tk.Button(self.shooting_frame, text="Weiter", command=restart_game)
        winner_label = tk.Label(self.shooting_frame, text=self.players[0].name + " gewinnt!")

        miss_label = tk.Label(self.shooting_frame, text="Daneben!")

        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        # TODO fix
        if quit:
            print("quit")
        if defeat:
            print("defeat")
            del self.players[self.get_active_player(1 * int(not quit))]
        else:
            if not first_time:
                miss_label.grid()
        if not quit and not first_time:
            self.active_player += 1
        next_player_label = tk.Label(self.shooting_frame,
                                     text="Nächster Spieler: " + self.players[self.get_active_player()].name)
        if len(self.players) == 1:  # Game ends.
            print("winner")
            winner_label.grid()
            winner_confirm.grid()
        else:
            print("no winner")
            next_player_label.grid()
            next_player_button.grid()

    def quit(self):
        """Whatever"""
        # TODO implement



def main():
    """Starts the game."""
    GameManager()


if __name__ == '__main__':
    main()
