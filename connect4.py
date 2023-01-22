import sys

class Color:
    BLACK = 1 
    RED   = 2

    
class Direction:

    DOWN  = 1
    LEFT_OR_RIGHT  = 2
    DIAGONAL_RIGHT = 3
    DIAGONAL_LEFT  = 4

    def __init__(self):
        self.directions = [Direction.DOWN,
                           Direction.LEFT_OR_RIGHT,
                           Direction.DIAGONAL_RIGHT,
                           Direction.DIAGONAL_LEFT]

    def getDirections(self):
        return self.directions
        
class Player:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return str(self.color)
        
class Game:
    def __init__(self):
        # r x c, ie board[row][col]
        # row 0 is bottom row
        self.board    = []
        self.MAX_ROWS = 6
        self.MAX_COLS = 7

        for r in range(0, self.MAX_ROWS):
            self.board.append([])
            for c in range(0, self.MAX_COLS):
                self.board[r].append(None)

        self.players = [Player(Color.BLACK), Player(Color.RED)]

    def isOccupied(self, row, column):
        if self.board[row][column] != None:
            return True

        return False

    # Need to return bool so user knows if accidentally drop in full column
    def canDropChecker(self, column):
        if column >= self.MAX_COLS or self.board[self.MAX_ROWS - 1][column] != None:
            return False
        else:
            return True
        
    # canDropChecker should be called before this 
    def dropChecker(self, column, color):
        # start at row 0, move up...
        for r in range(0,self.MAX_ROWS):
            if self.isOccupied(r, column):
                continue
            else:
                self.board[r][column] = color
                return self.is4Connected(r, column, color)

            
    # called when the checker is dropped...
    def is4Connected(self, r, c, color):
        directions_list = Direction().getDirections()
        for d in directions_list:
            if self.isFour(r, c, color, d):
                return True

        return False

    
    def isFour(self, r, c, color, direction):
        count = 0
        # we never have to look 'UP' since our checker will be at the
        # top of any vertical stack of connected by 4
        if direction == Direction.DOWN:
            for i in range(r, -1, -1):
                if self.board[i][c] == color:
                    count += 1
                else:
                    break

        # horizontal and diagonal are more tricky than DOWN,
        # can drop checker in middle of 4, need to check both
        # left and right
        elif direction == Direction.LEFT_OR_RIGHT:
            for i in range(c,-1,-1):
                if self.board[r][i] == color:
                    count += 1
                else:
                    break

            for i in range(c):
                if self.board[r][i] == color:
                    count += 1
                else:
                    break

        # different method here to the horizontal check,
        # just find starting and ending row/col vals,
        # and add 1 to each until end.  Reset count on mismatch.
        elif direction == Direction.DIAGONAL_RIGHT:
            row = r - c if r > c else 0
            col = c - r if c > r else 0
            
            while (row < self.MAX_ROWS and col < self.MAX_COLS):
                if self.board[row][col] == color:
                    count += 1
                    if count == 4:
                        break
                else:
                    count = 0

                row += 1
                col += 1

        elif direction == Direction.DIAGONAL_LEFT:
            row = r + c if r+c < self.MAX_ROWS else self.MAX_ROWS - 1
            col = c - (self.MAX_ROWS - r - 1) if c - (self.MAX_ROWS - r - 1) > 0 else 0
            
            # just want to decrement both r and c by 1 n times where
            # n = starting row - last row
            while (row > 0 and col < self.MAX_COLS):
                if self.board[row][col] == color:
                    count += 1
                    if count == 4:
                        break
                else:
                    count = 0
                # starting from left and going to the right...
                row -= 1
                col += 1
                    
        if count == 4:
            return True
        else:
            return False

    def __str__(self):
        # reverse iterate over indicies of self.board
        res = ""
        for r in range(len(self.board) - 1, -1, -1):
            # range is inclusive or something, so no need
            # to minus 1 on forward range
            for c in range(len(self.board[r])):
                # board initialized to None at each index
                if self.board[r][c] != None:
                    res += str(self.board[r][c])
                else:
                    res += " "
            res += '\n'
        return res
                

def getInputColumn():
    prompt = "Player %s which column to drop?" % str(player)
    col_str = input(prompt)
    if isinstance(col_str, int):
        return col_str
    
    col_str = col_str.rstrip()
    col = -1
    try:
        col = int(col_str)
        print("got " + str(col))

    except:
        print("Couldn't parse column... try again")
    print("returning " + str(col))
    return col
    
if __name__=="__main__":
    print("hello world!")

    game = Game()

    game_ended = False

    while not game_ended:

        for player in game.players:
            print(str(game))

            column = getInputColumn()

            if column == -1:
                print("can't parse the column provided, lose a turn!")
                continue
            
            if game.canDropChecker(column):
                print("Dropping to column " + str(column))
                game_ended = game.dropChecker(column, player.color)

            else:
                print("Column full, lose a turn!")                

            if game_ended:
                break                    

    print("Game Over!")
    
