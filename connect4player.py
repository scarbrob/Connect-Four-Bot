"""
This is a bot for connect 4. It takes two arguments, its ID (player 1 or 2) and a difficulty (positive integer). If a 0 or negative dificulty is entered it defaults to 1.
"""
__author__ = "Benjamin Scarbrough" 
__license__ = "MIT"
__date__ = "10/14/19"


# Imports
import random
import time
import math


class ComputerPlayer:
    """
    This is the class of the computer player.
    """


    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.quartets = None
        if(difficulty_level <= 0):
            self.plies = 1
        else:
            self.plies = difficulty_level
        self.player = id # set to ID
        self.opponent = 0 # set to 1 id ID is 2 and vice versa.
        if(self.player == 1):
            self.opponent = 2
        else:
            self.opponent = 1


    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0
        is on the bottom. It must return an int indicating in which column to
        drop a disc. It returns the best possible move, defined by the number of points.
        """
        # Calculate all the quartets
        if(self.quartets == None):
            self.quartets = self._calculate_quartets(rack)

        while True:
            move_rack = self._negamax(rack, self.plies, self.player)[0] # Get the rack of the move to make
            move = self._get_move(rack, move_rack) # Get the position that's different and get its column.
            if rack[move][-1] == 0: return move


    def _negamax(self, rack, depth, player):
        """
        The negamax algorithm. This is used to find the best move given the rack, and depth.
        """
        player_number = player
        opposite_number = 0
        if(player_number == 1):
            opposite_number = 2
        else:
            opposite_number = 1

        terminal = self._get_terminal_node(rack, player_number)
        if(depth == 0 or terminal): # the base case.
            return rack, self._calc_score(rack, player_number)

        score = -math.inf
        best_rack = None
        neighbors = self._get_neighbors(rack, player_number)
        for i in neighbors:
            new_score = -self._negamax(i, depth - 1, opposite_number)[1]
            if(new_score >= score): # Could probably implement a random pick when the two are equal.
                score = new_score
                best_rack = i

        return best_rack, score


    def _get_terminal_node(self, rack, player):
        """
        Check if teh rack is a terminal condition (the end condition). This is used in the _negamax method.
        """
        score = self._calc_score(rack, player)
        return score == math.inf or score == -math.inf or self._moves_left(rack) == False


    def _moves_left(self, rack):
        """
        Check if there are any valid moves left on the board. Return True or False. This is used in _get_terminal_node.
        """
        open_spaces = 0
        for i in range(len(rack)):
            if(self._is_valid_move(rack[i]) == False): # If the rack is full, don't bother checking it for open spaces.
                continue
            for j in range(len(rack[i])):
                if(rack[i][j] == 0):
                    open_spaces += 1 # For every open space add one.

        if(open_spaces == 0): # If there are no open spaces the rack is full.
            return False
        return True

        # height = rows
        # width = cols
    # horizontal = height * (width -3)
    # Vertical = width * (height -3)
    # rising diagonal = height -3 * width -3
    # falling diagonal = width -3 * height -3


    def _calculate_quartets(self, rack):
        """
        Calculate all quartets (move of 4 in a row that can be used to win).
        """
        rows = len(rack[0]) # height
        cols = len(rack)    # Length
        horizontals = []
        verticals = []
        rising_diagonals = []
        falling_diagonals = []

        # get the horizontal quartets
        for i in range(cols -3):
            for j in range(rows):
                temp = ((i,j), (i + 1,j), (i + 2,j), (i + 3,j))
                horizontals.append(temp)

        # Get the vertical quartets
        for i in range(cols):
            for j in range(rows - 3):
                temp = ((i,j), (i,j + 1), (i,j + 2), (i,j + 3))
                verticals.append(temp)

        # Get the rising diagonal quartets
        for i in range(cols - 3):
            for j in range(rows - 3):
                temp = ((i,j), (i + 1,j + 1), (i + 2,j + 2), (i + 3,j + 3))
                rising_diagonals.append(temp)

        # Get the falling diagonals
        for i in range(cols - 3):
            j = rows - 1 # Make it start at 0 instead of 1
            # Has to be a while loop because I couldn't get the -3 working with reverse()
            while j - 3 >= 0:
                temp = ((i,j), (i + 1,j - 1), (i + 2,j -2), (i + 3,j - 3))
                falling_diagonals.append(temp)
                j -= 1

        together = (horizontals + verticals + rising_diagonals + falling_diagonals)
        return tuple(map(tuple, together))


    def _calc_score(self, rack, player):
        """
        Calculates the score of a given rack, maximizes for the player, minimizes for the opponent.
        """
        quartets = self.quartets
        total = 0
        player2 = 2
        if(player == 2):
            player2 = 1

        for i in range(len(quartets)): # For each quartet...
            temp_total = 0
            num_ai = 0
            num_p2 = 0
            for j in range(len(quartets[i])): # For the length of each quartet i
                if(rack[quartets[i][j][0]][quartets[i][j][1]] == player): # If there is a 1, add 1 to num_ai
                    num_ai += 1
                if(rack[quartets[i][j][0]][quartets[i][j][1]] == player2): # if there is a 2 add 1 to num_p2
                    num_p2 += 1

            if(num_ai > 0 and num_p2 > 0): # If there is one of each in a quartet, it's score is zero.
                temp_total = 0
            elif(num_ai == 0 and num_p2 == 0): # If the quartet is empty, it's score is zero.
                temp_total = 0
            elif(num_ai > 0 and num_p2 == 0): # If ai is in the quartet and p2 isn't, for the amount of positions it occupies add points.
                if(num_ai == 1):
                    temp_total = 1
                elif(num_ai == 2):
                    temp_total = 10
                elif(num_ai == 3):
                    temp_total = 100
                elif(num_ai == 4):
                    return math.inf
            elif(num_p2 > 0 and num_ai == 0): # If p2 is in the quartet and ai isn't, for the amount of positions it occupies add negative points.
                if(num_p2 == 1):
                    temp_total = -1
                elif(num_p2 == 2):
                    temp_total = -10
                elif(num_p2 == 3):
                    temp_total = -100
                elif(num_p2 == 4):
                    return -math.inf

            total += temp_total # Add the quartet total to the overall total.
        return total


    def _is_valid_move(self, col):
        """
        Checks if there is a possible move in the given column. I.e. we don't want
        to place a tile in a column that's full.
        """
        return col[-1] == 0


    def _get_neighbors(self, rack, player):
        """
        Get all possible moves on the rack for the given plater. I.e. child nodes of the rack.
        """
        rows = len(rack[0]) # Height
        cols = len(rack)    # Length
        rack_list = list(map(list,rack))
        neighbor_racks = []

        # For the range in the rack, check if the row has any moves left, if it does add the player number to the lowest most row in the given column.
        for i in range(cols):
            if(self._is_valid_move(rack[i])):
                for j in range(rows):
                    if(rack_list[i][j] == 0):
                        rack_list[i][j] = player
                        break

                neighbor_racks.append(tuple(map(tuple,rack_list))) # Add the neighbor rack to a list.
                rack_list = list(map(list,rack)) # Set the main rack back to default.

        return tuple(map(tuple,neighbor_racks)) # Return the list of neighbors as tuples.


    def _get_move(self, rack, best_move):
        """
        Get the row that is different between rack and best_move (the best possible rack).
        """
        for i in range(len(rack)):
            for j in range(len(rack[i])):
                if(rack[i][j] != best_move[i][j]): # Return the spot where the two racks differ.
                    return i
