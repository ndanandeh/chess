""" Defines Pieces of the game: Chess"""

class Piece:
    """A simple base class for all pieces"""

    def __init__(self, color, position, name, temp):

        #color = "black" or "white" :: in graphics white = silver, black = gold
        self.color = color

        #current position in the board, tuple: (x,y) where x and y range from 0 to 7
        self.position = position

        #string of name of piece
        self.name = name

        #temporary identification: TODO: take out
        self.temp = temp


class Pawn(Piece):
    """The class for the Pawn Piece. Defines movement capability"""

    def __init__(self,color,position,name,temp):
        super().__init__(color,position,name,temp)

        #boolean value - True if pawn is susceptible to en passant move by enemy pawn
        #TODO: implement en passant fully
        self.enPassant = False

    def possible(self, destination, enemy=False):
        """ Checks if piece is allowed to move to desired position,
            not taking to account position of other pieces
            Input: destination - where piece is to be moved
                   enemy - True if a capture is occuring
            Output: True if move is possible(not taking into account other pieces
        """

        # check all possible (non-capture) white pawn moves
        if self.color == "white":
            if destination[0] == self.position[0]:
                if destination[1] == self.position[1] + 1:
                    return True
                # en passant
                elif self.position[1] == 1 and destination[1] == 3:
                    self.enPassant = True
                    return True
                else:
                    return False

            # check capture white pawn move
            elif enemy:
                if destination[0] == self.position[0] + 1 or destination[0] == self.position[0] - 1:
                    if destination[1] == self.position[1] + 1:
                        return True
            else:
                return False

        # check all possible (non-capture) black pawn moves
        else:
            if destination[0] == self.position[0]:
                if destination[1] == self.position[1] - 1:
                    return True
                # en passant
                elif self.position[1] == 6 and destination[1] == 4:
                    self.enPassant = True
                    return True
                else:
                    return False

            # check capture black pawn moves
            elif enemy == True:
                if destination[0] == self.position[0] + 1 or destination[0] == self.position[0] - 1:
                    if destination[1] == self.position[1] - 1:
                        return True
            else:
                return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
            input:  destination - final destination of piece
                    enemy - True if capturing capturing a piece
            output: List of tuples of positions traversed on the board in format (x,y)
        """

        path = []
        #if capturing a piece, no positions are traversed
        if (enemy and destination[0] != self.position[0]):
            return path

        #if moving down, append traversed positions to list
        if (self.position[1] < destination[1]):
            for i in range(self.position[1] + 1, destination[1] + 1):
                path.append((self.position[0], i))

        #if moving up, append traversed positions to list
        else:
            for i in range(destination[1], self.position[1]):
                path.append((self.position[0], i))

        return path


class Rook(Piece):
    """The class for the Rook Piece. Defines movement capability"""

    def __init__(self, color, position, name, temp):
        super().__init__(color, position, name, temp)

        #moved is set to True when the rook has been moved for the first time(used for castle determination)
        self.moved = False

    def possible(self, destination):
        """ Checks if piece is allowed to move to desired position,
            not taking to account position of other pieces
            Input:  destination - where piece is to be moved
            Output: True if move is possible(not taking into account other pieces
        """

        #If moving vertically, is possible
        if (destination[0] == self.position[0] and destination[1] != self.position[1]):
            return True
        #if moving horizontally, is possible
        if (destination[1] == self.position[1] and destination[0] != self.position[0]):
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
                  input:  destination - final destination of piece
                          enemy - True if capturing capturing a piece
                  output: List of tuples of positions traversed on the board in format (x,y)
              """

        path = []
        # moving vertical case
        if (self.position[0] == destination[0]):
            if (self.position[1] < destination[1]):
                for i in range(self.position[1] + 1, destination[1] + 1):
                    path.append((self.position[0], i))
            else:
                for i in range(destination[1], self.position[1]):
                    path.append((self.position[0], i))
        # moving horizontally case
        else:
            if (self.position[0] < destination[0]):
                for i in range(self.position[0] + 1, destination[0] + 1):
                    path.append((i, self.position[1]))
            else:
                for i in range(destination[0], self.position[0]):
                    path.append((i, self.position[1]))
        #if capturing, remove the last position(shouldn't be considered as a blocking piece)
        if (enemy):
            path.remove(tuple(destination))
        return path


class Bishop(Piece):
    """The class for the Bishop Piece. Defines movement capability"""

    def possible(self, destination):
        """ Checks if piece is allowed to move to desired position,
        not taking to account position of other pieces
        Input:  destination - where piece is to be moved
        Output: True if move is possible(not taking into account other pieces
        """

        #if movement is diagonal, then it is possible
        if (abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])):
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
                  input:  destination - final destination of piece
                          enemy - True if capturing capturing a piece
                  output: List of tuples of positions traversed on the board in format (x,y)
              """

        path = []
        if (self.position[0] < destination[0]):
            # up right case
            if (self.position[1] < destination[1]):
                for i in range(1, destination[0] - self.position[0] + 1):
                    path.append((self.position[0] + i, self.position[1] + i))
            # down right case
            else:
                for i in range(1, destination[0] - self.position[0] + 1):
                    path.append((self.position[0] + i, self.position[1] - i))
        else:
            # up left case
            if (self.position[1] < destination[1]):
                for i in range(1, destination[1] - self.position[1] + 1):
                    path.append((self.position[0] - i, self.position[1] + i))
            # down left case
            else:
                for i in range(1, self.position[0] - destination[0] + 1):
                    path.append((self.position[0] - i, self.position[1] - i))
        #if capturing, remove last position(shouldn't be considered as blocking piece)
        if (enemy):
            path.remove(tuple(destination))

        return path


class Knight(Piece):
    """The class for the Rook Piece. Defines movement capability"""

    def possible(self, destination):
        """ Checks if piece is allowed to move to desired position,
            not taking to account position of other pieces
            Input:  destination - where piece is to be moved
            Output: True if move is possible(not taking into account other pieces
        """

        #define various L shape movements as possible, and other movements as impossible
        if (abs(self.position[0] - destination[0]) == 1 and abs(self.position[1] - destination[1]) == 2):
            return True
        elif (abs(self.position[0] - destination[0]) == 2 and abs(self.position[1] - destination[1]) == 1):
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
                  input:  destination - final destination of piece
                          enemy - True if capturing capturing a piece
                  output: List of tuples of positions traversed on the board in format (x,y)
              """

        #can't block a knight(except at destination)
        path = [tuple(destination)]

        #if capturing, remove last position(shouldn't be considered a blocking piece)
        if (enemy):
            path.remove(tuple(destination))
        return path


class Queen(Piece):
    """The class for the Queen Piece. Defines movement capability"""

    def possible(self, destination):
        """ Checks if piece is allowed to move to desired position,
            not taking to account position of other pieces
            Input:  destination - where piece is to be moved
            Output: True if move is possible(not taking into account other pieces
        """

        #can move like bishop
        if (abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])):
            return True
        #can move like rook(vertical)
        elif (destination[0] == self.position[0] and destination[1] != self.position[1]):
            return True
        #can move like rook(horizontal)
        elif (destination[1] == self.position[1] and destination[0] != self.position[0]):
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
                  input:  destination - final destination of piece
                          enemy - True if capturing capturing a piece
                  output: List of tuples of positions traversed on the board in format (x,y)
              """

        path = []

        #if moving like a bishop
        if (abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])):
            if (self.position[0] < destination[0]):
                # up right case
                if (self.position[1] < destination[1]):
                    for i in range(1, destination[0] - self.position[0] + 1):
                        path.append((self.position[0] + i, self.position[1] + i))
                        # down right case
                else:
                    for i in range(1, destination[0] - self.position[0] + 1):
                        path.append((self.position[0] + i, self.position[1] - i))
            else:

                # up left case
                if (self.position[1] < destination[1]):
                    for i in range(1, destination[1] - self.position[1] + 1):
                        path.append((self.position[0] - i, self.position[1] + i))
                # down left case
                else:
                    for i in range(1, self.position[0] - destination[0] + 1):
                        path.append((self.position[0] - i, self.position[1] - i))

        #if moving like a rook
        else:
            # moving vertical case
            if (self.position[0] == destination[0]):
                if (self.position[1] < destination[1]):
                    for i in range(self.position[1] + 1, destination[1] + 1):
                        path.append((self.position[0], i))
                else:
                    for i in range(destination[1], self.position[1]):
                        path.append((self.position[0], i))
            # moving horizontally case
            else:
                if (self.position[0] < destination[0]):
                    for i in range(self.position[0] + 1, destination[0] + 1):
                        path.append((i, self.position[1]))
                else:
                    for i in range(destination[0], self.position[0]):
                        path.append((i, self.position[1]))

        #if capturing, remove last position (shouldn't be considered as a blocking piece)
        if (enemy):
            path.remove(tuple(destination))

        return path


class King(Piece):
    """The class for the King Piece. Defines movement capability"""

    def __init__(self, color, position, name, temp):
        super().__init__(color, position, name, temp)

        #moved is set to True when the rook has been moved for the first time(used for castle determination)
        self.moved = False

    def possible(self, destination):
        """ Checks if piece is allowed to move to desired position,
                   not taking to account position of other pieces
                   Input:  destination - where piece is to be moved
                   Output: True if move is possible(not taking into account other pieces
               """

        # diagonal move
        if (abs(destination[0] - self.position[0]) == 1 and abs(destination[1] - self.position[1]) == 1):
            return True
        # horizontal move
        if (abs(destination[0] - self.position[0]) == 1 and destination[1] == self.position[1]):
            return True
        # vertical move
        if (destination[0] == self.position[0] and abs(destination[1] - self.position[1]) == 1):
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        """returns list of board positions traversed by a piece to get to destination
                  input:  destination - final destination of piece
                          enemy - True if capturing capturing a piece
                  output: List of tuples of positions traversed on the board in format (x,y)
              """

        #if capturing remove, last position not considered as a blocking position
        if (not enemy):
            return [tuple(destination)]
        else:
            return []
