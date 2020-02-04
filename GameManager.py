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
        self.root.geometry("500x500")
        self.start_frame = tk.Frame(self.root)
        self.start_frame.grid()
        self.placement_frame = tk.Frame(self.root)
        tk.Label(self.start_frame, text=self.intro, justify="left").grid(row=0, column=0)
        tk.Button(self.start_frame, text="Start", command=self.start).grid(row=1, column=0)
        self.names_frame = tk.Frame(self.root)
        self.root.mainloop()

    def get_active_player(self):
        """Return the index of the active player."""
        return self.active_player % len(self.players)

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
                rnd.shuffle(self. players)
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
            self.next_shooting()
        else:
            self.players[self.get_active_player()].show_placing(self)
            self.active_player += 1

    def next_shooting(self):
        """"""
        if len(self.players) == 1:
            print(self.players[0] + " wins")
            # TODO implement
        else:
            self.players[self.get_active_player() + 1].show_shooting()
            self.players[self.get_active_player()].show_viewing()

def main():
    """Starts the game."""
    GameManager()


if __name__ == '__main__':
    main()
