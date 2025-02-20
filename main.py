import random
import os

def clear():
    os.system("cls")

class Game:
    def __init__(self, player_one_piece = "X", player_two_piece="O", blank="-"):
        self.player_one_piece = player_one_piece
        self.player_two_piece = player_two_piece
        self.blank = blank

        self.player_one_score = 0
        self.player_two_score = 0
        
        # i know i know but this works for now so back off
        self.board = [
            [self.blank, self.blank, self.blank],
            [self.blank, self.blank, self.blank],
            [self.blank, self.blank, self.blank]
        ]

    def print_board(self):
        print("   A B C")
        for i, row in enumerate(self.board):
            print(f"{i+1} ", end="")
            for column in row:
                print(f" {column}", end="")
            print()
        print(f"\n{self.player_one_piece} wins: {self.player_one_score}")
        print(f"{self.player_two_piece} wins: {self.player_two_score}\n")

    def get_next_move(self, player, is_computer=False):
        clear()
        if is_computer:
            next_move = self.decide_next_move(player)
            self.edit_board(next_move, player)
            return False
        
        valid_move = False
        while not valid_move:
            self.print_board()
            
            next_move = input(f"{player}'s next move: ")
            clear()
            if len(next_move) != 2:
                print("Invalid input length, try again.")
            elif not (next_move[0].lower() in ['a', 'b', 'c']):
                print("Invalid column, try again.")
            elif not (next_move[1] in ['1', '2', '3']):
                print("Invalid row, try again.")
            else:
                reformatted_next_move = [int(next_move[1]) - 1, ord(next_move[0].lower()) - ord('a')]
                blank_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.blank]
                if not (reformatted_next_move in blank_locations):
                    print("Invalid location, spot is already occupied, try again.")
                else:
                    self.edit_board(reformatted_next_move, player)
                    valid_move = True

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
                if column != self.blank:
                    continue
                
                possible_board = [row[:] for row in self.board]
                possible_board[row_index][column_index] = player
                if self.check_for_win(possible_board) == player:
                    return [row_index, column_index]
        return False

    def decide_next_move(self, computer_piece):
        player_piece = [piece for piece in [self.player_one_piece, self.player_two_piece] if piece != computer_piece][0]

        corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        edges = [[0, 1], [1, 0], [1, 2], [2, 1]]
        center = [1, 1]

        total_moves = len([column for row in self.board for column in row if not column == self.blank])
        player_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == player_piece]
        computer_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == computer_piece]
        blank_locations = [[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.blank]
        
        player_possible_win = self.check_possible_wins(player_piece)
        computer_possible_win = self.check_possible_wins(computer_piece)

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
            player_location = player_locations[0]
            if player_location == center:
                new_move = random.choice(corners)
            elif player_location in corners:
                new_move = center
            else:
                new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in player_one_location]
        
        # if the computer and player have each made a move
        elif total_moves == 2:
            if (player_locations[0] in corners) or (player_locations[0] in edges):
                new_move = center
            else: # if the player moved to the center play the reciprocal of the current computer move
                new_move = [2 if coord == 0 else random.choice([0, 2]) if coord == 1 else 0 for coord in computer_locations[0]]
        
        # if the player has 2 moves and the computer has only made one move
        elif total_moves == 3:
            # if the player has both in the corner
            if (player_locations[0] in corners) and (player_locations[1] in corners):
                new_move = random.choice(edges)
            # if the player has one in the center and one in the corner
            elif ((player_locations[0] in corners) and (player_locations[1] == center)) or (player_locations[1] in corners) and (player_locations[0] == center):
                new_move = random.choice(corners)
            # if the player has one in the edge and center
            elif ((player_locations[0] in edges) and (player_locations[1] in corners)) or ((player_locations[1] in edges) and (player_locations[0] in corners)):
                if self.board[1][1] == self.blank:
                    new_move = center
                else:
                    new_move = random.choice([corner for corner in corners if (corner != player_locations[0]) and (corner != player_locations[1])])

        # override any move that was made if a win is found for anyone next move
        if computer_possible_win:
            new_move = computer_possible_win
        elif player_possible_win:
            new_move = player_possible_win

        return new_move

    def reset_board(self):
        self.board = [
            [self.blank, self.blank, self.blank],
            [self.blank, self.blank, self.blank],
            [self.blank, self.blank, self.blank]
        ]

    def play_round(self, player_one_first, single_player):
        while True:
            if player_one_first:
                self.get_next_move(self.player_one_piece)
            else:
                self.get_next_move(self.player_two_piece, is_computer=single_player)
            player_one_first = not player_one_first
            
            win_check = self.check_for_win()
            if win_check:
                if win_check == self.player_one_piece:
                    self.player_one_score += 1
                elif win_check == self.player_two_piece:
                    self.player_two_score += 1
                self.print_board()
                print(f"{win_check} won this round")
                break
            elif len([[row, column] for row in range(len(self.board)) for column in range(len(self.board[row])) if self.board[row][column] == self.blank]) == 0:
                self.print_board()
                print("Tie game")
                break
    
    def run_game(self):
        clear()
        print("Welcome to Tic-Tac-Toe!")
        player_count = input("Would you like to do PvP or PvAI? [pvp/pvai]: ")

        if player_count == 'michaelbadfnafgame':
            clear()
            print("nuh uh")
            return False
        elif player_count == 'michealbadfnafgame':
            clear()
            print("nuh uh (also you spelled my name wrong nerd)")
            return False
        
        if not (player_count in ['pvp', 'pvai']):
            clear()
            print("Ok you dont play by the rules you dont play the game.")
            return False

        clear()
        player_one_first = True

        # yea yea i know i should make this its own function but whatever i need a v1.0 out
        if player_count == 'pvp':
            while True:
                self.play_round(player_one_first, single_player=False)
                player_one_first = not player_one_first

                continue_game = input("Continue playing? [q to quit]: ")
                if continue_game.lower() == 'q':
                    break
                self.reset_board()
        elif player_count == 'pvai':
            while True:
                self.play_round(player_one_first, single_player=True)
                player_one_first = not player_one_first

                continue_game = input("Continue playing? [q to quit]: ")
                if continue_game.lower() == 'q':
                    break
                self.reset_board()
        clear()
        print("Thanks for playing!")
        
game = Game()
game.run_game()