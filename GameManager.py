"""Provides the GameManager class."""

__author__ = "6601128, Schademan, 7232927, Tobias"
__credits__ = ""
__email__ = "schejda@googlemail.com, s0798915@rz.uni-frankfurt.de"

import tkinter as tk
import random as rnd
import tkinter.messagebox
from Player import Player


class GameManager:
    """Manages the game."""

    def __init__(self):
        """Initializes a GameManager"""
        self.active_player = 0
        self.players = []
        self.options = {"size": (10, 10), "shot_per_ship": False, "spray": False, "time": 30}
        self.intro = \
            """
Willkommen!
Für dieses Spiel gilt:
-Spieler schießen stets auf das Feld des jeweils danach
 schießenden Spielers.
-Es ist möglich, dass man Schiffe direkt nebeneinander platziert.
-Wenn ein Spieler aufgibt, ist das Spiel nicht beendet, 
 sondern wird unter den verbleibenden Spielern fortgeführt.
 Sollte danach nur noch ein Spieler übrig sein, endet das Spiel natürlich.
-Wenn während eines Zuges die Zeit abläuft, 
 ist der nächste Spieler an der Reihe.
"""
        self.root = tk.Tk()
        self.root.geometry("400x800+100+100")
        self.start_frame = tk.Frame(self.root)
        self.start_frame.grid()
        self.placement_frame = tk.Frame(self.root)
        self.shooting_frame = tk.Frame(self.root)
        self.names_frame = tk.Frame(self.root)
        self.options_frame = tk.Frame(self.root)
        self.open_main_menu()
        self.root.mainloop()

    def open_main_menu(self):
        """Displays the main menu"""
        tk.Label(self.start_frame, text=self.intro, justify="left").grid(row=0, column=0)
        tk.Button(self.start_frame, text="Start", command=self.start).grid(row=1, column=0)
        tk.Button(self.start_frame, text="Optionen", command=self.open_options).grid(row=2,
                                                                                     column=0)
        self.start_frame.grid()

    def open_options(self):
        """Opens the options menu."""

        def back():
            """Returns to the main menu."""

            if int(rows.get()) < 5 or int(columns.get()) < 5:
                tk.messagebox.showerror(title="Fehler", message="Spielfeld ist zu klein.")
            else:
                # Sets the options according to the inputs.
                self.options_frame.grid_forget()
                self.options["spray"] = spray.get()
                self.options["shot_per_ship"] = shot_per_ship.get()
                self.options["size"] = (int(rows.get()), int(columns.get()))
                self.options["time"] = int(time.get())
                self.open_main_menu()

        # The tk Vars are used for setting the input fields to the value
        # of the corresponding options value.
        rows = tk.StringVar()
        rows.set(self.options["size"][0])
        columns = tk.StringVar()
        columns.set(self.options["size"][1])
        spray = tk.BooleanVar()
        spray.set(self.options["spray"])
        shot_per_ship = tk.BooleanVar()
        shot_per_ship.set(self.options["shot_per_ship"])
        time = tk.StringVar()
        time.set(self.options["time"])

        self.start_frame.grid_forget()
        self.options_frame.grid()

        tk.Label(self.options_frame, text="Optionen").grid(row=0, column=0, columnspan=2)
        tk.Label(self.options_frame, text="Reihen").grid(row=1, column=0)
        tk.Entry(self.options_frame, textvariable=rows).grid(row=1, column=1)
        tk.Label(self.options_frame, text="Spalten").grid(row=2, column=0)
        tk.Entry(self.options_frame, textvariable=columns).grid(row=2, column=1)
        tk.Label(self.options_frame, text="Schuss pro Schiff").grid(row=3, column=0)
        tk.Checkbutton(self.options_frame, variable=shot_per_ship).grid(row=3, column=1)
        tk.Label(self.options_frame, text="Streuung").grid(row=4, column=0)
        tk.Checkbutton(self.options_frame, variable=spray).grid(row=4, column=1)
        tk.Label(self.options_frame, text="Bedenkzeit").grid(row=5, column=0)
        tk.Entry(self.options_frame, textvariable=time).grid(row=5, column=1)
        tk.Button(self.options_frame, text="Zurück", command=back).grid(row=6, column=0,
                                                                        columnspan=2)

    def get_active_player(self, offset=0):
        """Return the index of the active player."""
        return (self.active_player + offset) % len(self.players)

    def increase_active_player(self):
        """Increases the active player by 1.

        This is necessary because if this value is higher than the length
        of all players, a player might be skipped when a player gets deleted
        from the list.
        """
        self.active_player += 1
        self.active_player = self.active_player % len(self.players)

    def start(self):
        """Opens the menu to name the players."""

        self.start_frame.grid_forget()
        self.names_frame.grid()
        tk.Label(self.names_frame, text="Bitte Namen eingeben").grid(columnspan=3)
        player_name_entries = [
            (tk.Label(self.names_frame, text="Spieler "), tk.Entry(self.names_frame)),
            (tk.Label(self.names_frame, text="Spieler "), tk.Entry(self.names_frame))]
        # Displays the default two player entries.
        for i in range(len(player_name_entries)):
            player_name_entries[i][0]["text"] += str(i + 1) + ":"
            player_name_entries[i][0].grid(row=i + 2, column=0, columnspan=2, sticky="W")
            player_name_entries[i][1].grid(row=i + 2, column=2)

        def add_player():
            """Adds a player."""
            player_name_entries.append((tk.Label(self.names_frame, text="Spieler " + str(
                len(player_name_entries) + 1) + ":"), tk.Entry(self.names_frame)))
            player_name_entries[-1][0].grid(row=len(player_name_entries) + 2, column=0,
                                            columnspan=2, sticky="W")
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
                while len(player_name_entries) > 0:
                    entry = player_name_entries.pop()
                    self.players.append(
                        Player(entry[1].get(), (self.options["size"]), self.root, self))
                    entry[0].grid_forget()
                    entry[1].grid_forget()
                self.names_frame.grid_forget()
                # Shuffles players so that it is random who begins.
                rnd.shuffle(self.players)
                # Begins placement for the first player.
                self.next_placement()
            else:
                tk.messagebox.showerror(
                    "Für jeden Spieler muss ein Name eingegeben werden")

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
            # Start the shooting phase.
            self.next_shooting()
        else:
            # Let the next player place.
            self.players[self.get_active_player()].show_placing()
            self.increase_active_player()

    def next_shooting(self, miss=False, timeout=False, no_shots_left=False):
        """Starts the turn of the next player."""

        miss_label = tk.Label(self.shooting_frame, text="Daneben!")
        timeout_label = tk.Label(self.shooting_frame, text="Zeit abgelaufen!")
        no_shots_left_label = tk.Label(self.shooting_frame, text="Keine Schüsse übrig!")

        def show_shooting_view():
            """Displays the field of opponent and self."""
            self.shooting_frame.grid_forget()
            next_player_button.grid_forget()
            next_player_label.grid_forget()
            miss_label.grid_forget()
            timeout_label.grid_forget()
            no_shots_left_label.grid_forget()
            self.players[self.get_active_player(1)].show_shooting(
                self.players[self.get_active_player()])
            self.players[self.get_active_player()].show_viewing()

        def restart_game():
            """Opens the main menu and resets players."""
            winner_confirm.grid_forget()
            winner_label.grid_forget()
            self.shooting_frame.grid_forget()
            self.players = list()
            self.active_player = 0
            self.open_main_menu()

        self.shooting_frame.grid()
        next_player_button = tk.Button(self.shooting_frame, text="Bereit",
                                       command=show_shooting_view)
        winner_confirm = tk.Button(self.shooting_frame, text="Weiter", command=restart_game)
        winner_label = tk.Label(self.shooting_frame, text=self.players[0].name + " gewinnt!")

        if miss:
            miss_label.grid()
        elif timeout:
            timeout_label.grid()
        elif no_shots_left:
            no_shots_left_label.grid()

        next_player_label = tk.Label(self.shooting_frame, text="Nächster Spieler: " + self.players[
            self.get_active_player()].name)
        if len(self.players) == 1:  # Game ends.
            # Show winner.
            winner_label.grid()
            winner_confirm.grid()
        else:
            # Show who is next and display the "Bereit" button.
            next_player_label.grid()
            next_player_button.grid()

    def miss(self):
        """Continues with the next player."""
        self.players[self.get_active_player()].visible = False
        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        self.increase_active_player()
        self.next_shooting(miss=True)

    def quit(self):
        """Deletes the current player."""
        self.players[self.get_active_player()].visible = False
        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        self.players.pop(self.get_active_player())
        # No need for increasing active_player, because the current player
        # gets deleted from list and active_player therefore points
        # automatically to the next player who is now at the index of
        # former current player.
        self.next_shooting()

    def defeat(self):
        """Deletes the next player."""
        self.players[self.get_active_player()].visible = False
        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        self.players.pop(self.get_active_player(1))
        self.increase_active_player()
        self.next_shooting()

    def timeout(self):
        """Continues with the next player."""
        self.players[self.get_active_player()].visible = False
        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        self.increase_active_player()
        self.next_shooting(timeout=True)

    def no_shots_left(self):
        """Continues with the next player."""
        self.players[self.get_active_player()].visible = False
        self.players[self.get_active_player()].clear()
        self.players[self.get_active_player(1)].clear()
        self.increase_active_player()
        self.next_shooting(no_shots_left=True)


def main():
    """Starts the game."""
    GameManager()


if __name__ == '__main__':
    main()
