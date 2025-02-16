import random

board = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]

def print_board():
    print()
    for row in board:
        for column in row:
            print(f" {column}", end="")
        print()
    print()

def edit_board(coord, piece):
    board[coord[0]][coord[1]] = piece

def decide_next_move():
    player = "X"
    computer = "O"
    blank = "-"

    total_moves = len([column for row in board for column in row if not column == blank])
    player_move_locations = [(row, column) for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == player]
    computer_move_locations = [(row, column) for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == computer]
    
    if total_moves == 0:
        new_move = (random.choice([0, 2]), random.choice([0, 2]))
        edit_board(new_move, computer)

decide_next_move()
print_board()