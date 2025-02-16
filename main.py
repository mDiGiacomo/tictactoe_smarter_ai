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

def decide_next_move():
    pass

print_board()