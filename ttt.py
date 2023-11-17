from textwrap import fill
import tkinter as tk
from tkinter import messagebox
import random
from turtle import fillcolor
# size_of_board = 800
# symbol_size = (size_of_board / 3 - size_of_board / 8) / 2

window = tk.Tk()
window.title("PY-TTT")


board = [' ' for _ in range(9)]
current_player = 'X'
difficulty = 'Easy'  

def handle_click(index):
    global current_player

    
    if board[index] != ' ':
        messagebox.showerror("Invalid Move", "This position is already occupied! ❌")
        return

   
    board[index] = current_player
    buttons[index].config(text=current_player)

    
    if check_win(current_player):
        messagebox.showinfo("Game Over", f"Player {current_player} wins! 👑")
        reset_game()
        return

   
    if ' ' not in board:
        messagebox.showinfo("Game Over", "It's a draw! 🎳")
        reset_game()
        return

    
    current_player = 'O'
    computer_move()


def computer_move():
    global current_player

    if difficulty == 'Easy':
        easy_mode()
    elif difficulty == 'Normal':
        normal_mode()
    elif difficulty == 'Hard':
        hard_mode()

   
    if check_win('O'):
        messagebox.showinfo("Game Over", "Computer wins! 👑")
        reset_game()
        return

    if ' ' not in board:
        messagebox.showinfo("Game Over", "It's a draw! 🎳")
        reset_game()
        return

    
    current_player = 'X'


def easy_mode():
    while True:
        index = random.randint(0, 8)
        if board[index] == ' ':
            board[index] = current_player
            buttons[index].config(text=current_player)
            break


def normal_mode():
    
    for i in range(9):
        if board[i] == ' ':
            board[i] = current_player
            if check_win(current_player):
                buttons[i].config(text=current_player)
                return
            else:
                board[i] = ' '

    
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_win('X'):
                board[i] = current_player
                buttons[i].config(text=current_player)
                return
            else:
                board[i] = ' '

    easy_mode()


def hard_mode():
    best_score = float('-inf')
    best_move = None

    for i in range(9):
        if board[i] == ' ':
            board[i] = current_player
            score = minimax(board, 0, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i

    board[best_move] = current_player
    buttons[best_move].config(text=current_player)


def minimax(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'draw': 0}

    if check_win('X'):
        return scores['X']
    elif check_win('O'):
        return scores['O']
    elif ' ' not in board:
        return scores['draw']

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score


def check_win(player):
   
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == player:
            return True
    
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == player:
            return True
   
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    return False


def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    for button in buttons:
        button.config(text=' ')


def change_difficulty(level):
    global difficulty
    difficulty = level


buttons = []
for i in range(9):
    button = tk.Button(window, text=' ', font=('Arial', 20), width=6, height=3,
                       command=lambda i=i: handle_click(i))
    button.configure(bg="#33C4FF", fg = "#000000", width=7, height=3)
    # button.after(bg = "#1287B7")
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)


difficulty_frame = tk.Frame(window)
difficulty_frame.grid(row=3, columnspan=3, pady=10)

easy_button = tk.Button(difficulty_frame, text='Easy', font=('Arial', 14), width=8,
                        command=lambda: change_difficulty('Easy'))
easy_button.pack(side=tk.LEFT, padx=5)
easy_button.configure(bg= "#FFCE33")
normal_button = tk.Button(difficulty_frame, text='Normal', font=('Arial', 14), width=8,
                          command=lambda: change_difficulty('Normal'))
normal_button.pack(side=tk.LEFT, padx=5)
normal_button.configure(bg= "#33FF4F")

hard_button = tk.Button(difficulty_frame, text='Hard', font=('Arial', 14), width=8,
                        command=lambda: change_difficulty('Hard'))
hard_button.pack(side=tk.LEFT, padx=5)
hard_button.configure(bg= "#FF3333")


window.mainloop()