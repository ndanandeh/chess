import piece
from tkinter import *

#create empty board
board = [[0 for i in range(8)] for k in range(8)]
#place black pawns
for i in range (8):
    board[i][6] = piece.Pawn("black", (i,6), "pawn","bp")

#place white pawns
for i in range(8):
    board[i][1] = piece.Pawn("white",(i,1),"pawn","wp")

#place white rooks
for (a,b) in [(0,0), (7,0)]:
    board[a][b] = piece.Rook("white",(a,b),"rook","wr")

#place black rooks
for (a,b) in [(0,7), (7,7)]:
    board[a][b] = piece.Rook("black",(a,b), "rook","br")

#place white bishops
for (a,b) in [(2,0), (5,0)]:
    board[a][b] = piece.Bishop("white",(a,b),"bishop","wb")

#place black bishops
for (a,b) in [(2,7), (5,7)]:
    board[a][b] = piece.Bishop("black",(a,b),"bishop","bb")

#place white knights
for (a,b) in [(1,0), (6,0)]:
    board[a][b] = piece.Knight("white",(a,b),"knight","wk")

#place black knights
for (a,b) in [(1,7), (6,7)]:
    board[a][b] = piece.Knight("black",(a,b),"knight","bk")

#place white queen
board[3][0] = piece.Queen("white", (3,0), "queen","wQ")

#place black queen
board[3][7] = piece.Queen("black", (3,7), "queen", "bQ")

#place white king
board[4][0] = piece.King("white", (4,0), "king", "wKi")

#place black king
board[4][7] = piece.King("black", (4,7), "king", "bKi")

def movePiece(pos, dest):
    board[dest[0]][dest[1]] = board[pos[0]][pos[1]]
    board[pos[0]][pos[1]] = 0
    board[dest[0]][dest[1]].position = (dest[0],dest[1])




def checkTraverse(pos,dest):
    #is capture
    if( isinstance(board[dest[0]][dest[1]],piece.Piece) and board[pos[0]][pos[1]].color != board[dest[0]][dest[1]].color):
        return board[pos[0]][pos[1]].traverse(dest, True)
        print("Capturing Piece")
    #is not capture
    else:
        return board[pos[0]][pos[1]].traverse(dest)

def checkPossible(pos,dest):
    if( isinstance(board[pos[0]][pos[1]], piece.Pawn)):
        if( isinstance(board[dest[0]][dest[1]],piece.Piece) and board[pos[0]][pos[1]].color != board[dest[0]][dest[1]].color):
            return board[pos[0]][pos[1]].possible(dest,True)
    return board[pos[0]][pos[1]].possible(dest)


def checkCheck(pos,color):
    pass

gameOn = True


root = Tk()

w = Label(root, text = "Hello , world!")
w.pack()

root.mainloop()

#start gameloop
while(gameOn):

    moveSuccess = True

    print("============================================")
    for k in range(8):
        for i in range(8):
            if(isinstance(board[i][k],piece.Piece)):
                print('{:5}'.format(board[i][k].temp),end='')
            else:
                print('{:5}'.format('x'),end='')

        print('')
    print("============================================")

    move = [int(x) for x in input("Enter Move:     ").split()]

    try:
        if(len(move) != 4 ) :
            raise Exception('incorrect # of inputs')
    except Exception:
        print("Must enter 4 nums, Try again ")
        continue
        
    if (not isinstance(board[move[0]][move[1]], piece.Piece)):
        print("Enter space with Piece on it, Try again")
        continue
    

    if(checkPossible(move[:2],move[2:])):
        traverse = checkTraverse(move[:2], move[2:])
        for (a,b) in traverse:
            print('{} {}'.format(a,b))
            if(isinstance(board[a][b],piece.Piece)):
                moveSuccess = False
                print("failed Traverse")
                break
    else:
        moveSuccess = False


    if (moveSuccess):
        movePiece(move[:2],move[2:])

    else: 
        print("Move Failure")

