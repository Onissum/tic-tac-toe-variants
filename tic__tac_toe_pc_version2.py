import tkinter as tk
import random

window = tk.Tk()
window.title("Tic Tac Toe")

turn = "X"
grid = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
play_again_window = None  # Aggiungo una variabile globale per la finestra "Vuoi giocare ancora?"

# Creo l'etichetta del turno
label = tk.Label(window, text=f"Turno di {turn}", font=("Arial", 24))
label.grid(row=3, column=0, columnspan=3)

def disable_all_buttons():
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)  # Disabilito il pulsante dopo aver fatto una mossa

# Creo i pulsanti della griglia
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(window, text="", font=("Arial", 24), width=5, height=2,
                                  command=lambda row=i, col=j: on_button_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Creo una funzione che gestisce il clic su un pulsante
def on_button_click(row, col):
    global turn
    if grid[row][col] == "":
        grid[row][col] = turn
        buttons[row][col].config(text=turn)
        buttons[row][col].config(state=tk.DISABLED)
        if check_winner(turn):
            announce_winner(turn)
        elif check_draw():
            announce_draw()
        else:
            if turn == "X":
                turn = "O"
            else:
                turn = "X"
            label.config(text=f"Turno di {turn}")
            if mode == "1P" and turn == "O":
                # E' il turno del computer
                computer_move()

def check_winner(player):
    # Verifica se il giocatore ha vinto
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] == player or \
           grid[0][i] == grid[1][i] == grid[2][i] == player:
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] == player or \
       grid[0][2] == grid[1][1] == grid[2][0] == player:
        return True
    return False

def announce_winner(player):
    label.config(text=f"Giocatore {player} ha vinto!")
    disable_all_buttons()
    if mode == "1P" and player == "O":
        ask_play_again("Hai perso! Vuoi giocare ancora?")

def check_draw():
    # Verifica se la partita è finita in pareggio
    for row in grid:
        if "" in row:
            return False
    return True

def announce_draw():
    label.config(text="Pareggio!")
    disable_all_buttons()
    if mode == "1P":
        ask_play_again("Pareggio! Vuoi giocare ancora?")

def computer_move():
    best_score = float("-inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if grid[i][j] == "":
                grid[i][j] = "O"
                score = minimax(grid, 0, False)
                grid[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    if best_move:
        row, col = best_move
        on_button_click(row, col)

def minimax(board, depth, is_maximizing):
    scores = {
        "X": -1,
        "O": 1,
        "tie": 0
    }

    if check_winner("X"):
        return scores["X"]

    if check_winner("O"):
        return scores["O"]

    if check_draw():
        return scores["tie"]

    if is_maximizing:
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def ask_play_again(result):
    global play_again_window
    play_again_window = tk.Toplevel(window)
    play_again_window.title("Vuoi giocare ancora?")
    play_again_label = tk.Label(play_again_window, text=result, font=("Arial", 16))
    play_again_label.pack(padx=10, pady=10)

    play_again_button = tk.Button(play_again_window, text="Gioca di nuovo", font=("Arial", 16),
                                  command=restart_game)
    play_again_button.pack(padx=10, pady=10)

    exit_button = tk.Button(play_again_window, text="Esci", font=("Arial", 16),
                            command=quit_game)
    exit_button.pack(padx=10, pady=10)

# Creo una funzione che chiude la finestra secondaria della modalità di gioco
def close_mode_window():
    global mode_window
    mode_window.destroy()

# Creo una funzione che chiede al giocatore la modalità di gioco
def ask_mode():
    global mode_window, mode  # Rendo la variabile mode_window globale
    mode = None  # Inizializzo la modalità come None
    # Creo una finestra secondaria
    mode_window = tk.Toplevel(window)
    mode_window.title("Scegli la modalità di gioco")
    # Creo due pulsanti per scegliere la modalità di gioco
    button_1P = tk.Button(mode_window, text="VS. AI", font=("Arial", 16), width=10, height=2,
                          command=lambda: set_mode("1P"))
    button_2P = tk.Button(mode_window, text="2 giocatori", font=("Arial", 16), width=10, height=2,
                          command=lambda: set_mode("2P"))
    button_1P.pack(padx=10, pady=10)
    button_2P.pack(padx=10, pady=10)
    # Aggiungere un pulsante per chiudere la finestra secondaria
    button_close = tk.Button(mode_window, text="Chiudi", font=("Arial", 16),
                            command=close_mode_window)
    button_close.pack(padx=10, pady=10)

# Creo una funzione che imposta la modalità di gioco e chiude la finestra secondaria
def set_mode(m):
    global mode, mode_window  # Rendo le variabili mode e mode_window globali
    mode = m
    mode_window.destroy()
    if mode == "1P":
        computer_move()

# Creo una funzione che riavvia il gioco
def restart_game():
    global grid, turn
    turn = "X"
    # Resetta griglia
    for i in range(3):
        for j in range(3):
            grid[i][j] = ""
            buttons[i][j].config(text="")
            buttons[i][j].config(state=tk.NORMAL)  # Riabilita tutti i pulsanti
    label.config(text=f"Turno di {turn}")
    if mode == "1P" and turn == "O":
        computer_move()
    # Chiudo la finestra "Vuoi giocare ancora?"
    play_again_window.destroy()

# Creo una funzione che chiude il gioco
def quit_game():
    play_again_window.destroy()
    window.destroy()

# Chiamo la funzione che chiede al giocatore la modalità di gioco
ask_mode()

# Avvio il ciclo principale della finestra
window.mainloop()
