import tkinter as tk
from tkinter import font as tkfont
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x700")
        # Colors
        self.bg_color = "#2C3E50"  # Dark blue background
        self.margin_color = "#34495E"  # Slightly lighter blue for margins
        self.border_color = "#E74C3C"  # Red border
        self.x_color = "#3498DB"  # Blue for X
        self.o_color = "#2ECC71"  # Green for O
        self.text_color = "#ECF0F1"  # White text
        self.winner_color = "#F1C40F"  # Yellow for winner highlight
        
        # Set window background
        self.root.configure(bg=self.bg_color)
        
        # Initialize game variables
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.score_font = tkfont.Font(family="Helvetica", size=16)
        self.button_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        title_frame.pack(fill="x")
        
        title_label = tk.Label(
            title_frame, 
            text="Tic Tac Toe",
            font=self.title_font,
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack()
        
        # Scoreboard
        self.score_frame = tk.Frame(self.root, bg=self.margin_color, padx=20, pady=10)
        self.score_frame.pack(fill="x", padx=20, pady=10)
        
        # Player X score
        x_score_label = tk.Label(
            self.score_frame,
            text="Player X:",
            font=self.score_font,
            fg=self.x_color,
            bg=self.margin_color
        )
        x_score_label.grid(row=0, column=0, padx=10)
        
        self.x_score_value = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            fg=self.x_color,
            bg=self.margin_color
        )
        self.x_score_value.grid(row=0, column=1, padx=10)
        
        # Ties score
        ties_label = tk.Label(
            self.score_frame,
            text="Ties:",
            font=self.score_font,
            fg=self.text_color,
            bg=self.margin_color
        )
        ties_label.grid(row=0, column=2, padx=10)
        
        self.ties_value = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            fg=self.text_color,
            bg=self.margin_color
        )
        self.ties_value.grid(row=0, column=3, padx=10)
        
        # Player O score
        o_score_label = tk.Label(
            self.score_frame,
            text="Player O:",
            font=self.score_font,
            fg=self.o_color,
            bg=self.margin_color
        )
        o_score_label.grid(row=0, column=4, padx=10)
        
        self.o_score_value = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            fg=self.o_color,
            bg=self.margin_color
        )
        self.o_score_value.grid(row=0, column=5, padx=10)
        
        # Status label
        self.status_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        self.status_frame.pack(fill="x")
        
        self.status_label = tk.Label(
            self.status_frame,
            text=f"Player {self.current_player}'s Turn",
            font=self.status_font,
            fg=self.x_color if self.current_player == "X" else self.o_color,
            bg=self.bg_color
        )
        self.status_label.pack()
        
        # Game board (3x3 grid)
        self.board_frame = tk.Frame(
            self.root,
            bg=self.border_color,
            padx=3,
            pady=3,
        )
        self.board_frame.pack(padx=50, pady=20)
        
        # Create buttons for the game board
        self.buttons = []
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=self.button_font,
                    width=3,
                    height=1,
                    bg=self.margin_color,
                    fg=self.text_color,
                    activebackground=self.margin_color,
                    relief=tk.RAISED,
                    borderwidth=2,
                    command=lambda idx=idx: self.make_move(idx)
                )
                button.grid(row=i, column=j, padx=3, pady=3, ipadx=20, ipady=20)
                self.buttons.append(button)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        control_frame.pack(fill="x")
        
        restart_button = tk.Button(
            control_frame,
            text="Restart Game",
            font=self.score_font,
            bg=self.margin_color,
            fg=self.text_color,
            padx=10,
            pady=5,
            command=self.restart_game
        )
        restart_button.pack(side=tk.LEFT, padx=20, pady=10, expand=True)
        
        reset_score_button = tk.Button(
            control_frame,
            text="Reset Scores",
            font=self.score_font,
            bg=self.margin_color,
            fg=self.text_color,
            padx=10,
            pady=5,
            command=self.reset_scores
        )
        reset_score_button.pack(side=tk.RIGHT, padx=20, pady=10, expand=True)
        
        # Add AI toggle button
        self.ai_enabled = False
        self.ai_button = tk.Button(
            self.root,
            text="Play Against AI (Off)",
            font=self.score_font,
            bg=self.margin_color,
            fg=self.text_color,
            padx=10,
            pady=5,
            command=self.toggle_ai
        )
        self.ai_button.pack(pady=10)
    
    def make_move(self, idx):
        # Check if the move is valid and game is not over
        if self.board[idx] == "" and not self.game_over:
            # Update the board
            self.board[idx] = self.current_player
            self.buttons[idx].config(
                text=self.current_player,
                fg=self.x_color if self.current_player == "X" else self.o_color
            )
            
            # Check for win or tie
            winner = self.check_winner()
            if winner:
                self.game_over = True
                if winner == "Tie":
                    self.scores["Ties"] += 1
                    self.ties_value.config(text=str(self.scores["Ties"]))
                    self.status_label.config(text="Game Tied!", fg=self.text_color)
                else:
                    self.scores[winner] += 1
                    if winner == "X":
                        self.x_score_value.config(text=str(self.scores["X"]))
                    else:
                        self.o_score_value.config(text=str(self.scores["O"]))
                    
                    self.status_label.config(
                        text=f"Player {winner} Wins!",
                        fg=self.winner_color
                    )
                    
                    # Highlight winning cells
                    for i in self.get_winning_cells():
                        self.buttons[i].config(bg=self.winner_color)
            else:
                # Switch player
                self.current_player = "O" if self.current_player == "X" else "X"
                player_color = self.o_color if self.current_player == "O" else self.x_color
                self.status_label.config(text=f"Player {self.current_player}'s Turn", fg=player_color)
                
                # AI move if enabled and it's O's turn
                if self.ai_enabled and self.current_player == "O" and not self.game_over:
                    self.root.after(500, self.ai_move)
    
    def ai_move(self):
        # Simple AI: First try to win, then block, then random move
        empty_cells = [i for i in range(9) if self.board[i] == ""]
        
        # Check if AI can win
        for cell in empty_cells:
            self.board[cell] = "O"
            if self.check_winner() == "O":
                self.make_move(cell)
                return
            self.board[cell] = ""
        
        # Block player's winning move
        for cell in empty_cells:
            self.board[cell] = "X"
            if self.check_winner() == "X":
                self.board[cell] = ""
                self.make_move(cell)
                return
            self.board[cell] = ""
        
        # Make a random move
        if empty_cells:
            cell = random.choice(empty_cells)
            self.make_move(cell)
    
    def check_winner(self):
        # Define winning combinations
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        # Check for a win
        for combo in win_combinations:
            if (self.board[combo[0]] != "" and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return self.board[combo[0]]
        
        # Check for a tie
        if "" not in self.board:
            return "Tie"
        
        # Game continues
        return None
    
    def get_winning_cells(self):
        # Define winning combinations
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        # Find the winning combination
        for combo in win_combinations:
            if (self.board[combo[0]] != "" and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return combo
        
        return []
    
    def restart_game(self):
        # Reset game variables
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        
        # Reset buttons
        for button in self.buttons:
            button.config(text="", bg=self.margin_color)
        
        # Update status label
        self.status_label.config(text=f"Player {self.current_player}'s Turn", fg=self.x_color)
    
    def reset_scores(self):
        # Reset scores
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self.x_score_value.config(text="0")
        self.o_score_value.config(text="0")
        self.ties_value.config(text="0")
        
        # Restart the game
        self.restart_game()
    
    def toggle_ai(self):
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.ai_button.config(text="Play Against AI (On)")
            # If it's O's turn, make an AI move
            if self.current_player == "O" and not self.game_over:
                self.root.after(500, self.ai_move)
        else:
            self.ai_button.config(text="Play Against AI (Off)")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
            
    
