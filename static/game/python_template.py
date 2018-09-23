class move: #class for denoting a move
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    
    def __init__(self, a, b, c, d):
        self.x1 = a
        self.y1 = b
        self.x2 = c
        self.y2 = d

board = [[0,0,0,0,0],   #Your board
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0]]

def initBoard():    #Function to initialize the board
    global board
    for i in range(5):
        board[0][i] = 'B'
        board[1][i] = 'b'
        board[2][i] = '_'
        board[3][i] = 'r'
        board[4][i] = 'R'

def findBestMove():
    #returns the move you want to make 
    
def mValidation():
    #validates your sample move according to the given rules in the documentation

def makemove ():
    #makes move temporarily

def undoMove():
    #undoes the temporarily made move

def algorithm():
    #your game's algorithm

def evaluate():
    #evaluation for your move
    
initBoard()
turn = None
turn = input()
#if turn = 1, you are Sentinels and it's your turn first
#if turn = 0, you are Scourges and it's opponent's turn first
whoAmI=turn

while(1):
    
    if turn!=1:
        input = raw_input()
        #Input from opponent
        #Use this input to make changes in your board
        
    turn = 0
    #after first iteration, (turn!=1) is always true
    #i.e. turn is always 0
    
    #your logic to make the next move
    #output your move string
    print(output)
    
"""
 * x = ['x1 ', 'y1 ', 'x2 ', 'y2']
 * y = ['x1 ', 'y1 ', 'x2 ', 'y2']
 *
 * Your code outputs a string of length 7 containing 4 characters each
 * separated by a space, where x1 & y1 are respective row and column
 * of your piece's initial position and x2 & y2 are respective row and
 * column of your piece's final position.
 *
 * Each of x1,y1,x2,y2 must be >=0 and <5.
 *
 * Consider "B"-> Sentinels' bombers "b"-> Sentinels' stingers (Blue)
 * 			"R"-> Scourges' bombers "r"-> Scourges' stingers   (Red)
 * 			"_"-> Empty space
 * 
 * Board representation:
 *
 * B B B B B
 * b b b b b
 * _ _ _ _ _
 * r r r r r
 * R R R R R
 *
 * Note:- The program will be terminated automatically when either player wins.
"""

