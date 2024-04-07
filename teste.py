import random
import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, name):
        self.name = name
        self.passes = {}
    
    def add_pass(self, player):
        if player in self.passes:
            self.passes[player] += 1
        else:
            self.passes[player] = 1
    
    def get_pass_probability(self, player):
        total_passes = sum(self.passes.values())
        if player in self.passes:
            return self.passes[player] / total_passes
        else:
            return 0
        
class BasketballMatch:
    def __init__(self, players):
        self.players = {player.name: player for player in players}
    
    def simulate_match(self, num_passes):
        current_player = random.choice(list(self.players.keys()))
        for _ in range(num_passes):
            next_player = self.choose_next_player(current_player)
            self.players[current_player].add_pass(next_player)
            current_player = next_player
    
    def choose_next_player(self, current_player):
        probabilities = [self.players[current_player].get_pass_probability(player) for player in self.players]
        return random.choices(list(self.players.keys()), probabilities)[0]
    
    def eliminate_least_frequent_passes(self, threshold):
        for player in self.players.values():
            passes_to_remove = [p for p, count in player.passes.items() if count <= threshold]
            for p in passes_to_remove:
                del player.passes[p]
    
    def is_player_crucial(self, player_name):
        if player_name not in self.players:
            return False
        
        player = self.players[player_name]
        if len(player.passes) == 0:
            return False
        
        for other_player in self.players.values():
            if player_name in other_player.passes:
                return True
        
        return False
class BasketballMatchGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Basketball Match Simulator")
        
        self.players = []
        
        self.player_entry = tk.Entry(self.window)
        self.player_entry.pack()
        self.add_player_button = tk.Button(self.window, text="Add Player", command=self.add_player)
        self.add_player_button.pack()
        
        self.player1_var = tk.StringVar()
        self.player2_var = tk.StringVar()
        self.player1_dropdown = tk.OptionMenu(self.window, self.player1_var, "")
        self.player1_dropdown.pack()
        self.player2_dropdown = tk.OptionMenu(self.window, self.player2_var, "")
        self.player2_dropdown.pack()
        self.add_pass_button = tk.Button(self.window, text="Add Pass", command=self.add_pass)
        self.add_pass_button.pack()
        
        self.simulate_button = tk.Button(self.window, text="Simulate Match", command=self.simulate_match)
        self.simulate_button.pack()
        
        self.eliminate_button = tk.Button(self.window, text="Eliminate Least Frequent Passes", command=self.eliminate_passes)
        self.eliminate_button.pack()
        
        self.check_crucial_button = tk.Button(self.window, text="Check Crucial Players", command=self.check_crucial_players)
        self.check_crucial_button.pack()
    
    def add_player(self):
        player_name = self.player_entry.get()
        if player_name:
            player = Player(player_name)
            self.players.append(player)
            self.player1_dropdown["menu"].add_command(label=player_name, command=tk._setit(self.player1_var, player_name))
            self.player2_dropdown["menu"].add_command(label=player_name, command=tk._setit(self.player2_var, player_name))
            self.player_entry.delete(0, tk.END)
    
    def add_pass(self):
        player1_name = self.player1_var.get()
        player2_name = self.player2_var.get()
        if player1_name and player2_name:
            player1 = next((p for p in self.players if p.name == player1_name), None)
            player2 = next((p for p in self.players if p.name == player2_name), None)
            if player1 and player2:
                player1.add_pass(player2_name)
    
    def simulate_match(self):
        match = BasketballMatch(self.players)
        match.simulate_match(1000)
        messagebox.showinfo("Match Simulation", "Match simulated successfully!")
    
    def eliminate_passes(self):
        match = BasketballMatch(self.players)
        match.eliminate_least_frequent_passes(50)
        messagebox.showinfo("Pass Elimination", "Least frequent passes eliminated!")
    
    def check_crucial_players(self):
        match = BasketballMatch(self.players)
        crucial_players = [player.name for player in self.players if match.is_player_crucial(player.name)]
        messagebox.showinfo("Crucial Players", f"Crucial players: {', '.join(crucial_players)}")
    
    def run(self):
        self.window.mainloop()

# Run the GUI
gui = BasketballMatchGUI()
gui.run()
