import random

class Game:
    def __init__(self, player_one_piece = "X", player_two_piece="O", blank="-"):
        self.player_one_piece = player_one_piece
        self.player_two_piece = player_two_piece
        self.blank = blank
        self.board = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]
        ]

    def print_board(self):
        print()
        for row in self.board:
            for column in row:
                print(f" {column}", end="")
            print()
        print()

    def edit_board(self, coord, piece):
        self.board[coord[0]][coord[1]] = piece

    def check_for_win(self, board=None):
        if board == None:
            board = self.board

        for player in [self.player_one_piece, self.player_two_piece]:
            rows = [row for row in board if len(set(row)) == 1 and set(row) == {player}]
            columns = [row for row in [list(x) for x in zip(*board)] if len(set(row)) == 1 and set(row) == {player}]
            left_diagonal = len(set([item for sublist in board for item in sublist][::4])) and set([item for sublist in board for item in sublist][::4]) == {player}
            right_diagonal = len(set([item for sublist in board for item in sublist][2::2][:3])) and set([item for sublist in board for item in sublist][2::2][:3]) == {player}

            if rows or columns or left_diagonal or right_diagonal:
                return player
        return False

    def check_possible_wins(self, player):
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(row):
                if column != blank:
                    continue
                
                possible_board = [row[:] for row in self.board]
                possible_board[row_index][column_index] = player
                if check_for_win(possible_board) == player:
                    return [row_index, column_index]
        return False

    def decide_next_move(self):
        corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        edges = [[0, 1], [1, 0], [1, 2], [2, 1]]
        center = [1, 1]

        total_moves = len([column for row in self.board for column in row if not column == self.blank])
        player_one_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.player_one_piece]
        player_two_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.player_two_piece]
        blank_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.blank]
        
        player_one_possible_win = check_possible_wins(self.player_one_piece)
        player_two_possible_win = check_possible_wins(self.player_two_piece)

        # make a valid random move to have a default move ready
        while True:
            coord = random.choice(blank_locations)
            if self.board[coord[0]][coord[1]] == self.blank:
                new_move = coord
                break
        
        # if the computer gets the first move put the piece in the corners
        if total_moves == 0:
            new_move = random.choice(corners)

        # if the player gets the first move
        elif total_moves == 1:
            player_one_location = player_one_locations[0]
            if player_one_location == center:
                new_move = random.choice(corners)
            elif player_one_location in corners:
                new_move = center
            else:
                new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in player_one_location]
        
        # if the computer and player have each made a move
        elif total_moves == 2:
            if (player_one_locations[0] in corners) or (player_one_locations[0] in edges):
                new_move = center
            else: # if the player moved to the center play the reciprocal of the current computer move
                new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in player_two_locations[0]]
        
        # if the player has 2 moves and the computer has only made one move
        elif total_moves == 3:
            # if the player has both in the corner
            if (player_one_locations[0] in corners) and (player_one_locations[1] in corners):
                new_move = random.choice(edges)
            # if the player has one in the center and one in the corner
            elif ((player_one_locations[0] in corners) and (player_one_locations[1] == center)) or (player_one_locations[1] in corners) and (player_one_locations[0] == center):
                new_move = random.choice(corners)
            # if the player has one in the edge and center
            elif ((player_one_locations[0] in edges) and (player_one_locations[1] in corners)) or ((player_one_locations[1] in edges) and (player_one_locations[0] in corners)):
                if board[1][1] == blank:
                    new_move = center
                else:
                    new_move = random.choice([corner for corner in corners if (corner != player_one_locations[0]) and (corner != player_one_locations[1])])

        # override any move that was made if a win is found for either player next round
        if player_one_possible_win:
            new_move = player_one_possible_win
        elif player_two_possible_win:
            new_move = player_two_possible_win

        edit_board(new_move, self.computer)

game = Game()