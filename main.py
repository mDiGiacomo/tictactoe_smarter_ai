board = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]

def print_board(board):
    print()
    for row in board:
        for column in row:
            print(f" {column}", end="")
        print()
    print()
    
print_board(board)