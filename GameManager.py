"""Provides the GameManager class."""

# header

import tkinter as tk
from Player import Player


class GameManager:
    """Manages the game."""

    def __init__(self):
        """Initializes a GameManager"""
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

        def name_players():
            """Creates all players according to their names."""
            if all(player[1].get() != "" for player in player_name_entries):
                for player in player_name_entries:
                    self.players.append(Player(player[1].get(), (self.options["size"]), self.root))
                    self.names_frame.grid_forget()
                self.players[0].show_placing()
            else:
                print("error")

        add = tk.Button(self.names_frame, text="+", command=add_player)
        add.grid(row=1, column=0, sticky="WE")
        remove = tk.Button(self.names_frame, text="-", command=remove_player)
        remove.grid(row=1, column=1, sticky="WE")
        go_next = tk.Button(self.names_frame, text="Weiter", command=name_players)
        go_next.grid(row=1, column=2)


def main():
    """Starts the game."""
    GameManager()


if __name__ == '__main__':
    main()
