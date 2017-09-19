import piece

class Board:
    """defines board for Chess game, and controls interactions between pieces"""

    def __init__(self):

        # create empty board, and populate it
        self.board = [[0 for i in range(8)] for k in range(8)]
        # place black pawns
        for i in range(8):
            self.board[i][6] = piece.Pawn("black", (i, 6), "pawn", "bp")
        # place white pawns
        for i in range(8):
            self.board[i][1] = piece.Pawn("white", (i, 1), "pawn", "wp")
        # place white rooks
        for (a, b) in [(0, 0), (7, 0)]:
            self.board[a][b] = piece.Rook("white", (a, b), "rook", "wr")
        # place black rooks
        for (a, b) in [(0, 7), (7, 7)]:
            self.board[a][b] = piece.Rook("black", (a, b), "rook", "br")
        # place white bishops
        for (a, b) in [(2, 0), (5, 0)]:
            self.board[a][b] = piece.Bishop("white", (a, b), "bishop", "wb")
        # place black bishops
        for (a, b) in [(2, 7), (5, 7)]:
            self.board[a][b] = piece.Bishop("black", (a, b), "bishop", "bb")
        # place white knights
        for (a, b) in [(1, 0), (6, 0)]:
            self.board[a][b] = piece.Knight("white", (a, b), "knight", "wk")
        # place black knights
        for (a, b) in [(1, 7), (6, 7)]:
            self.board[a][b] = piece.Knight("black", (a, b), "knight", "bk")
        # place white queen
        self.board[3][0] = piece.Queen("white", (3, 0), "queen", "wQ")
        # place black queen
        self.board[3][7] = piece.Queen("black", (3, 7), "queen", "bQ")
        # place white king
        self.board[4][0] = piece.King("white", (4, 0), "king", "wKi")
        # place black king
        self.board[4][7] = piece.King("black", (4, 7), "king", "bKi")

        #positions of kings to check for check status
        self.kingPos = [(4, 0), (4, 7)]

        #check if game is over
        self.checkMate = False

        #keep track of # of turns(even or odd for whose turn it is
        self.turn = 0

        #Turned to True if En Passant is possible in current turn
        self.passant = False

    def movePiece(self,pos, dest):
        """moves a piece on the board(taking into account castle and en passant)
            input:  pos - current position of piece : (x,y) format
                    dest - position where piece should be moved to: (x,y) format
        """

        #set passant every turn to check if en passant is possible
        if(isinstance(self.board[pos[0]][pos[1]],piece.Pawn)):
            if(self.board[pos[0]][pos[1]].enPassant == True):
                self.passant = True
        else:
            self.passant = False

        #check if castle move
        if(not self.checkPossible(pos,dest)):
            if(pos == self.kingPos[0]):
                if(dest == (1,0)):
                    self.board[2][0] = self.board[0][0]
                    self.board[2][0].position = (2,0)
                    self.board[0][0] = 0
                elif(dest == (6,0)):
                    self.board[5][0] = self.board[7][0]
                    self.board[5][0].position = (5,0)
                    self.board[7][0] = 0
            elif(pos == self.kingPos[1]):
                if(dest == (1,7)):
                    self.board[2][7] = self.board[0][7]
                    self.board[2][7].position = (2,7)
                    self.board[0][7] = 0
                elif(dest ==(6,7)):
                    print("Final Step")
                    self.board[5][7] = self.board[7][7]
                    self.board[5][7].position = (5,7)
                    self.board[7][7] = 0

        # move piece(normally)
        self.board[dest[0]][dest[1]] = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = 0
        self.board[dest[0]][dest[1]].position = (dest[0], dest[1])

    def checkTraverse(self,pos, dest):
        """Controls traverse functions of pieces by deciding if a capture is occuring or not
            inputs: pos - current position of piece
                    dest - position where piece is moving
        """

        # is capture
        if (isinstance(self.board[dest[0]][dest[1]], piece.Piece) and self.board[pos[0]][pos[1]].color != self.board[dest[0]][
            dest[1]].color):
            return self.board[pos[0]][pos[1]].traverse(dest, True)
        # is not capture
        else:
            return self.board[pos[0]][pos[1]].traverse(dest)

    def checkPossible(self,pos, dest):
        """Controls possible function of pieces by deciding if extra input arguments are needed(for pawn)
            inputs: pos - currnet position of piece
                    dest - position where piece is moving
        """

        #if pawn and capturing piece "enemy" argument of piece is True
        if (isinstance(self.board[pos[0]][pos[1]], piece.Pawn)):
            if (isinstance(self.board[dest[0]][dest[1]], piece.Piece) and self.board[pos[0]][pos[1]].color != self.board[dest[0]][
                dest[1]].color):
                return self.board[pos[0]][pos[1]].possible(dest, True)
        return self.board[pos[0]][pos[1]].possible(dest)

    def checkMove(self,pos, dest):
        """Combines checkPossible with checkTraverse and returns true or false based on if movement is legal"""

        #check if move is possible
        if (not self.checkPossible(pos, dest)):
            return False

        #check if piece can traverse without being blocked by other piece on board
        else:
            traverse = self.checkTraverse(pos, dest)
            for (a, b) in traverse:
                if (isinstance(self.board[a][b], piece.Piece)):
                    return False
        return True

    def checkCheck(self,pos, color):
        """Looks at full board and sees if any pieces are able to capture piece at position pos
        inputs:     pos - position of piece to be captured
                    color - color of piece to be captured
        output:     checkList - List of all pieces on the board that can capture piece located at pos
        """

        checkList = []

        #Loop through board and check if anything can capture piece at pos
        for k in range(8):
            for i in range(8):
                if (isinstance(self.board[i][k], piece.Piece) and self.board[i][k].color != color):
                    if (self.checkMove(self.board[i][k].position, pos)):
                        checkList.append(self.board[i][k])

        return checkList

    def updateKingPos(self):
        """Updates positions of the two kings on the board. kingPos[0] = white king. kingPos[1] = black king"""

        for k in range(8):
            for i in range(8):
                if (isinstance(self.board[i][k], piece.King)):
                    if(self.board[i][k].color == "white"):
                        self.kingPos[0] = (i,k)
                    else:
                        self.kingPos[1] = (i,k)

    def castle(self,color,side):
        """Checks if castle is possible, assuming already that king has not moved
            inputs:     color - Color of the king you are castling: "white" or "black"
                        side - side of the castle: "left" or "right"
            output:     True if castle is possible in color/side. False otherwise
        """

        #checks if black castle is possible to right/left
        if(color == "black"):
            if(side == "right" and self.board[5][7] == 0 and self.board[6][7] == 0 and
            isinstance(self.board[7][7],piece.Rook) and not self.board[7][7].moved):
                return True
            elif(side == "left" and self.board[1][7] == 0 and self.board[2][7] == 0 and
                self.board[3][7] == 0 and isinstance(self.board[0][7],piece.Rook)
                 and not self.board[0][7].moved):
                return True

        #checks if white castle is possible to right/left
        if(color=="white"):
            if (side == "right" and self.board[5][0] == 0 and self.board[6][0] == 0 and
                    isinstance(self.board[7][0], piece.Rook) and not self.board[7][0].moved):
                return True
            elif (side == "left" and self.board[1][0] == 0 and self.board[2][0] == 0 and
                self.board[3][0] == 0 and isinstance(self.board[0][0], piece.Rook)
                  and not self.board[0][0].moved):
                return True

        return False

    def moveKing(self, king,color):
        """Generates a list of legal king moves
            inputs: king - position of king to generate list of moves
                    color - color of king to generate list of moves
        """

        moveList = []
        for i in range(-1,2):
            for k in range(-1,2):
                if (i==k==0):
                    break
                dest = (king[0]+i, king[1]+k)
                if(dest[0] <0 or dest[1] <0 or dest[0]>7 or dest[1]>7):
                    break
                if(self.checkMove(king,dest)):
                    temp = self.checkCheck(dest,color)
                    if(len(temp) == 0):
                        moveList.append((king,dest))

        return moveList

    def blockOrKill(self,target,pos):
        """Generates a list of moves that can kill piece at position target or block piece at position target
            from getting to position pos."""

        blockorKillList = []

        # repurpose check function to check if target can be killed
        killList = self.checkCheck(target.position,target.color)
        for i in range(len(killList)):
            blockorKillList.append((killList[i].position,target.position))


        #list of squares between target(piece checking) and pos(king)
        preBlockList = self.checkTraverse(target.position,pos)
        for i in  range(len(preBlockList)):
            #list of pieces that can move to preBlockList
            temp = self.checkCheck(preBlockList[i],target.color)
            for k in range(len(temp)):
                blockorKillList.append((temp[k].position,preBlockList[i]))

        return blockorKillList

    def completeMoveCheck(self,pos, dest):
        """Master move function: The function that links together all of the functions above
            and checks if a move is legal
            Inputs: pos - position of piece to move
                    dest - destination of piece to move
            Output: True if move is legal. False otherwise
        """

        # update position of kings
        self.updateKingPos()

        # check if clicking on non-piece square
        if (not isinstance(self.board[pos[0]][pos[1]], piece.Piece)):
            return False

        # get color of piece for easy use
        color = self.board[pos[0]][pos[1]].color

        # check if moving on correct turn
        if (self.turn % 2 == 0 and color == "white"):
            return False
        if (self.turn % 2 == 1 and color == "black"):
            return False

        # moving piece to same spot
        if (pos == dest):
            return False

        # check castle
        if (pos == (4, 0) and isinstance(self.board[pos[0]][pos[1]], piece.King) and not self.board[pos[0]][
            pos[1]].moved):
            print("check one")
            if (dest == (1, 0)):
                if (self.castle("white", "left")):
                    return True
            if (dest == (6, 0)):
                if (self.castle("white", "right")):
                    return True
        elif (pos == (4, 7) and isinstance(self.board[pos[0]][pos[1]], piece.King) and not self.board[pos[0]][
            pos[1]].moved):
            if (dest == (1, 7)):
                if (self.castle("black", "left")):
                    return True
            if (dest == (6, 7)):
                if (self.castle("black", "right")):
                    return True

        #check if valid move
        if (not self.checkMove(pos, dest)):
            return False

        #check if king under-check(before move) and generate list of legal moves if this is the case
        underCheck = False
        moveList = []
        if (color == "black"):
            checkList = self.checkCheck(self.kingPos[1], color)
            if (len(checkList) == 1):
                moveList.extend(self.blockOrKill(checkList[0],self.kingPos[1]))
            if(len(checkList)>0):
                underCheck = True
                moveList.extend(self.moveKing(self.kingPos[1],color))
        elif (color == "white"):
            checkList = self.checkCheck(self.kingPos[0], color)
            if (len(checkList) == 1):
                moveList.extend(self.blockOrKill(checkList[0], self.kingPos[0]))
            if (len(checkList) > 0):
                underCheck = True
                moveList.extend(self.moveKing(self.kingPos[0],color))

        #check if move will move you into check from check(illegal or mate)
        for i in range(len(moveList)):
            badMove = False
            temp = self.board[moveList[i][1][0]][moveList[i][1][1]]
            self.movePiece(moveList[i][0],moveList[i][1])
            self.updateKingPos()
            if(color == "white"):
                if(self.checkCheck(self.kingPos[0],color)):
                    badMove = True
            else:
                if(self.checkCheck(self.kingPos[1],color)):
                    badMove = True
            self.movePiece(moveList[i][1],moveList[i][0])
            self.board[moveList[i][1][0]][moveList[i][1][1]] = temp
            self.updateKingPos()

            if(badMove == True):
                moveList[i] = 0

        #remove moves from moveList that put you back into check
        for i in moveList:
            if(i==0):
                moveList.remove(0)

        #if under check and no moves that bring you out of check, game is over
        if(underCheck):
            if(len(moveList)==0):
                self.checkMate = True
            elif(not (pos,dest) in moveList):
                return False

        #not in check but move into check is illegal
        else:
            failed = False
            temp = self.board[dest[0]][dest[1]]
            self.movePiece(pos,dest)
            self.updateKingPos()
            if(color == "white"):
                if(len(self.checkCheck(self.kingPos[0],color)) != 0 ):
                    failed = True
            else:
                if(len(self.checkCheck(self.kingPos[1],color)) != 0):
                    failed = True

            self.movePiece(dest,pos)
            self.board[dest[0]][dest[1]] = temp
            self.updateKingPos()
            if(failed):
                return False

        #end of turn
        self.turn += 1
        return True



    #getter functions:

    def getBoard(self):
        return self.board

    def getTurn(self):
        return self.turn

    def getMate(self):
        return self.checkMate