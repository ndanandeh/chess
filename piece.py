""" Defines Pieces of the game: Chess"""

class Piece:
    """A simple base class for all pieces"""
    def __init__(self, color, position,name,temp):
        self.color = color
        self.position = position
        self.name = name	
        self.temp = temp

class Pawn(Piece):
    """The class for the Pawn Piece. Defines movement capability"""
    def possible(self,destination,enemy=False):
        """ Checks if piece is allowed to move to desired position,
            not taking to account position of other pieces """
	# check all possible (non-capture) white pawn moves
        if self.color == "white":
            if destination[0] == self.position[0]:
                if destination[1] == self.position[1]+1:
                    return True
	        #en passant
                elif self.position[1] == 1 and destination[1] == 3:
                    self.Passant = True
                    return True
                else:
                    return False
            #capture 
            elif enemy == True:
                if destination[0] == self.position[0] + 1 or destination[0] == self.position[0]-1:
                    if destination[1] == self.position[1]+1:
                        return True
            else:
                return False
	# check all possible (non-capture) black pawn moves
        else:
            if destination[0] == self.position[0]:
                if destination[1] == self.position[1]-1:
                    return True
	        #en passant
                elif self.position[1] == 6 and destination[1] == 4:
                    self.Passant = True
                    return True
                else:
                    return False
            #capture
            elif enemy == True:
                if destination[0] == self.position[0] +1 or destination[0] == self.position[0] -1:
                    if destination[1] == self.position[1] -1:
                        return True
            else:
                return False


    def traverse(self, destination, enemy = False):
        path = []
        if(enemy):
            return path
        if(self.position[1] < destination[1]):
            for i in range(self.position[1]+1,destination[1]+1):
                path.append((self.position[0],i))
        else:
            for i in range(destination[1],self.position[1]):
                path.append((self.position[0],i))

        return path
        
   
class Rook(Piece):
    """The class for the Rook Piece. Defines movement capability"""
    def possible(self,destination):
        if(destination[0] == self.position[0] and destination[1] != self.position[1]):
            return True
        if(destination[1] == self.position[1] and destination[0] != self.position[0]):
            return True
        else:
            return False

    def traverse(self,destination,enemy=False):
        path = []
        #moving vertical case
        if(self.position[0] == destination[0]):
            if(self.position[1] < destination[1]):
                for i in range(self.position[1]+1, destination[1]+1):
                    path.append((self.position[0],i))
            else:
                for i in range(destination[1], self.position[1]):
                    path.append((self.position[0],i))
        #moving horizontally case
        else:
            if(self.position[0]<destination[0]):
                for i in range(self.position[0]+1, destination[0]+1):
                    path.append((i,self.position[1]))
            else:
                for i in range(destination[0], self.position[0]):
                    path.append((i,self.position[1]))

        if(enemy):
            path.remove(tuple(destination))
        return path 



class Bishop(Piece):
    """The class for the Bishop Piece. Defines movement capability"""
    def possible(self,destination):
        if(abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])) : 
            return True
        else:
            return False

    def traverse(self, destination, enemy=False):
        path = []
        if(self.position[0]<destination[0]):
            #up right case
            if(self.position[1]<destination[1]):
                for i in range(1,destination[0] - self.position[0]+1):
                    path.append((self.position[0]+i, self.position[1]+i))
            #down right case
            else:
                for i in range(1,destination[0]-self.position[0]+1):
                    path.append((self.position[0]+i, self.position[1]-i))
        else:
            #up left case
            if(self.position[1]<destination[1]):
                for i in range(1,destination[1]-self.position[1]+1):
                    path.append((self.position[0]-i,self.position[1]+i))
            #down left case
            else:
                for i in range(1,self.position[0] - destination[0] + 1):
                    path.append((self.position[0]-i,self.position[1]-i))
   
        if(enemy):
            path.remove(tuple(destination))

        return path

class Knight(Piece):
    """The class for the Rook Piece. Defines movement capability"""
    def possible(self,destination):
        if(abs(self.position[0] - destination[0]) == 1 and abs(self.position[1] - destination[1]) == 2):
            return True
        elif (abs(self.position[0] - destination[0]) == 2 and abs(self.position[1] - destination[1]) == 1):
            return True
        else: 
            return False

    def traverse(self,destination,enemy=False):
        path = [tuple(destination)]
        if(enemy):
            path.remove(tuple(destination))
        return path




class Queen(Piece):
    def possible(self,destination):
        if(abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])) : 
            return True
        elif(destination[0] == self.position[0] and destination[1] != self.position[1]):
            return True
        elif(destination[1] == self.position[1] and destination[0] != self.position[0]):
            return True
        else:
            return False

    def traverse(self,destination,enemy=False):
        path = []
        
        if(abs(self.position[0] - destination[0]) == abs(self.position[1] - destination[1])) :
            if(self.position[0]<destination[0]):
	        #up right case
                if(self.position[1]<destination[1]):
                    for i in range(1,destination[0] - self.position[0]+1):
                        path.append((self.position[0]+i, self.position[1]+i))
                    #down right case
                else:
                    for i in range(1,destination[0]-self.position[0]+1):
                        path.append((self.position[0]+i, self.position[1]-i))
            else:

                #up left case
                if(self.position[1]<destination[1]):
                    for i in range(1,destination[1]-self.position[1]+1):
                        path.append((self.position[0]-i,self.position[1]+i))
                #down left case
                else:
                    for i in range(1,self.position[0] - destination[0] + 1):
                        path.append((self.position[0]-i,self.position[1]-i))

        else:
            #moving vertical case
            if(self.position[0] == destination[0]):
                if(self.position[1] < destination[1]):
                    for i in range(self.position[1]+1, destination[1]+1):
                        path.append((self.position[0],i))
                else:
                    for i in range(destination[1], self.position[1]):
                        path.append((self.position[0],i))
            #moving horizontally case
            else:
                if(self.position[0]<destination[0]):
                    for i in range(self.position[0]+1, destination[0]+1):
                        path.append((i,self.position[1]))
                else:
                    for i in range(destination[0], self.position[0]):
                        path.append((i,self.position[1]))

        if(enemy):
            path.remove(tuple(destination))
           
        return path

class King(Piece):
    def possible(self,destination):
        
        #diagonal move
        if(abs(destination[0] - self.position[0]) == 1 and abs(destination[1] - self.position[1]) == 1):
            return True
        #horizontal move
        if(abs(destination[0] -self.position[0]) == 1 and destination[1] == self.position[1]):
            return True
        #vertical move
        if(destination[0] == self.position[0] and abs(destination[1] - self.position[1]) == 1 ):
            return True
        else:
            return False

    def traverse(self, destination,enemy=False):
        if(not enemy):
            return [tuple(destination)]
        else:
            return []

