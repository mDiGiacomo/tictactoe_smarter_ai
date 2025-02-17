import random

board = [
    ["X", "-", "-"],
    ["-", "O", "-"],
    ["-", "X", "-"]
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

def check_for_win(board=board):
    player = "X"
    computer = "O"

    for user in [player, computer]:
        rows = [row for row in board if len(set(row)) == 1 and set(row) == {user}]
        columns = [row for row in [list(x) for x in zip(*board)] if len(set(row)) == 1 and set(row) == {user}]
        left_diagonal = len(set([item for sublist in board for item in sublist][::4])) and set([item for sublist in board for item in sublist][::4]) == {user}
        right_diagonal = len(set([item for sublist in board for item in sublist][2::2][:3])) and set([item for sublist in board for item in sublist][2::2][:3]) == {user}
        
        #print(f"{rows}\n{columns}\n{left_diagonal}\n{right_diagonal}")

        if rows or columns or left_diagonal or right_diagonal:
            return user

    return False

def check_possible_wins(user):
    blank = '-'

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            if column != blank:
                continue
            
            possible_board = [row[:] for row in board]
            possible_board[row_index][column_index] = user
            if check_for_win(possible_board) == user:
                return [row_index, column_index]
    
    return False

def decide_next_move():
    player = "X"
    computer = "O"
    blank = "-"
    corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
    edges = [[0, 1], [1, 0], [1, 2], [2, 1]]
    center = [1, 1]

    total_moves = len([column for row in board for column in row if not column == blank])
    player_locations = [[row, column] for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == player]
    computer_locations = [[row, column] for row in range(len(board)) for column in range(len(board[row])) if board[row][column] == computer]
    
    player_possible_win = check_possible_wins(player)
    computer_possible_win = check_possible_wins(computer)

    # make a valid random move to have a default move ready
    while True:
        coord = [random.randint(0, 2), random.randint(0, 2)]
        if board[coord[0]][coord[1]] == '-':
            new_move = coord
            break

    if total_moves == 0:
        new_move = (random.choice([0, 2]), random.choice([0, 2]))
        edit_board(new_move, computer)
    elif total_moves == 1:
        player_location = player_locations[0]
        if player_location == center:
            new_move = random.choice(corners)
        elif player_location in corners:
            new_move = center
        else:
            new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in player_location]
            print(new_move)
    elif total_moves == 2:
        pass
    elif total_moves == 3:
        # if the player has both in the corner
        if (player_locations[0] in corners) and (player_locations[1] in corners):
            new_move = random.choice(edges)
        # if the player has one in the center and one in the corner
        elif ((player_locations[0] in corners) and (player_locations[1] == center)) or (player_locations[1] in corners) and (player_locations[0] == center):
            new_move = random.choice(corners)
        # if the player has one in the edge and center
        elif ((player_locations[0] in edges) and (player_locations[1] in corners)) or ((player_locations[1] in edges) and (player_locations[0] in corners)):
            if board[1][1] == blank:
                new_move = center
            else:
                new_move = random.choice([corner for corner in corners if (corner != player_locations[0]) and (corner != player_locations[1])])

    # override any move that was made if a win is found for either player next round
    if computer_possible_win:
        new_move = computer_possible_win
    elif player_possible_win:
        new_move = player_possible_win

    edit_board(new_move, computer)

decide_next_move()
print_board()