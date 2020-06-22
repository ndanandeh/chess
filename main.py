import piece
import board
from tkinter import *
from tkinter import font


class Graphics():
    """Creates the Visuals for the Chess Game"""

    def __init__(self):
        # constants for image size
        self.squareSize = 83
        self.offset = 20

        # window creation and settings
        self.window = Tk()
        self.window.title('Chess- by Nathaniel Danandeh')
        self.canvas = Canvas(self.window, width=800, height=800, bg="white")

        # import images from assets folder
        self.boardIm = PhotoImage(file='assets/board.gif')
        self.whitePawnIm = PhotoImage(file='assets/white_pawn.gif')
        self.blackPawnIm = PhotoImage(file='assets/black_pawn.gif')
        self.whiteRookIm = PhotoImage(file='assets/white_rook.gif')
        self.blackRookIm = PhotoImage(file='assets/black_rook.gif')
        self.whiteKnightIm = PhotoImage(file='assets/white_knight.gif')
        self.blackKnightIm = PhotoImage(file='assets/black_knight.gif')
        self.whiteBishopIm = PhotoImage(file='assets/white_bishop.gif')
        self.blackBishopIm = PhotoImage(file='assets/black_bishop.gif')
        self.whiteQueenIm = PhotoImage(file='assets/white_queen.gif')
        self.blackQueenIm = PhotoImage(file='assets/black_queen.gif')
        self.whiteKingIm = PhotoImage(file='assets/white_king.gif')
        self.blackKingIm = PhotoImage(file='assets/black_king.gif')
        self.selectedIm = PhotoImage(file='assets/selected.gif')

        # Create instance of game logic that the GUI gets info from
        self.gameLogic = board.Board()

    def gameOver(self):
        """ Creates "Game Over" text on the screen """
        helv50 = font.Font(family='Helvetica', size=50, weight='bold')
        self.canvas.create_text(400, 400, text='Game Over', font=helv50, fill='red')
        self.canvas.pack()

    def update(self, turn):
        """ main graphics update function. Looks at state of game board and updates visuals accordingly
        input: turn - # of turns in the game(determines whose turn it is currently)"""

        # rename constants and board for ease of use
        board = self.gameLogic.getBoard()
        squareSize = self.squareSize
        offset = self.offset

        # draw the board image on the canvas
        self.canvas.create_image(400, 400, image=self.boardIm)

        # Print the color whose turn it is at the top left of the screen
        self.canvas.create_text(15, 10, text="Turn:")
        if (turn % 2 == 0):
            self.canvas.create_text(50, 10, text="gold")
        else:
            self.canvas.create_text(50, 10, text="silver")

        # draw all the pieces as they appear on the logic board
        for k in range(8):
            for i in range(8):
                if (isinstance(board[i][k], piece.Piece)):
                    if (board[i][k].name == 'pawn'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whitePawnIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackPawnIm)
                    elif (board[i][k].name == 'bishop'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whiteBishopIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackBishopIm)
                    elif (board[i][k].name == 'knight'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whiteKnightIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackKnightIm)
                    elif (board[i][k].name == 'rook'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whiteRookIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackRookIm)

                    elif (board[i][k].name == 'queen'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whiteQueenIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackQueenIm)

                    elif (board[i][k].name == 'king'):
                        if (board[i][k].color == 'white'):
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.whiteKingIm)
                        else:
                            self.canvas.create_image(board[i][k].position[0] * squareSize + squareSize + offset,
                                                     board[i][k].position[1] * squareSize + squareSize + offset,
                                                     image=self.blackKingIm)

                else:
                    continue


################################# END OF GRAPHICS CLASS #################################


moveList = []  # list of moves made
clickNum = 0  # number of clicks on the window so far
graphics = Graphics()  # instance of Graphics class


def callback(event):
    """Function that occurs on clicks of the window """

    # define variables used and increment click number
    global clickNum
    gameLogic = graphics.gameLogic
    clickNum = clickNum + 1

    # get the move from the click
    moveList.append((int(event.x / graphics.squareSize - 1), int(event.y / graphics.squareSize - 1)))

    # Create a red square around the chosen piece
    graphics.canvas.create_image((moveList[-1][0] + 1) * graphics.squareSize + graphics.offset,
                                 (moveList[-1][1] + 1) * graphics.squareSize + graphics.offset,
                                 image=graphics.selectedIm)
    graphics.canvas.pack()

    # if second click (a move) then check if valid, move piece, and update graphics
    if (clickNum % 2 == 0):
        if (gameLogic.completeMoveCheck(moveList[-2], moveList[-1])):
            gameLogic.movePiece(moveList[-2], moveList[-1])
            graphics.canvas.delete("all")
            graphics.update(gameLogic.getTurn())
            graphics.canvas.pack()

            # check if game is over
            if (gameLogic.getMate()):
                graphics.gameOver()
        else:

            # if move is not valid, remove last two moves from list and refresh graphics
            moveList.pop()
            moveList.pop()
            graphics.canvas.delete("all")
            graphics.update(gameLogic.getTurn())
            graphics.canvas.pack()


# bind a the callback function to the canvas
graphics.canvas.bind("<Button-1>", callback)

# call first update of the graphics (before any clicks occur)
graphics.update(graphics.gameLogic.getTurn())
graphics.canvas.pack()

# start the main window, and game, loop
graphics.window.mainloop()
