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
    corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
    edges = [[0, 1], [1, 0], [1, 2], [2, 1]]

    total_moves = len([column for row in board for column in row if not column == blank])
    player_locations = [[row, column] for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == player]
    computer_locations = [[row, column] for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == computer]
    
    if total_moves == 0:
        new_move = (random.choice([0, 2]), random.choice([0, 2]))
        edit_board(new_move, computer)
    elif total_moves == 1:
        player_location = player_locations[0]
        if player_location == [1, 1]:
            new_move = (random.choice([0, 2]), random.choice([0, 2]))
        elif player_location in corners:
            new_move = [1, 1]
        else:
            new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in player_location]
            print(new_move)

    edit_board(new_move, computer)

decide_next_move()
print_board()