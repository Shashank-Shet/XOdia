def board_initialise():       #function to initialize the board
    board = [[0 for x in range(2)] for y in range(8)]
    board[0][0] = 6
    board[7][1] = 6
    for i in range(1,7):
        for j in range(2):
            board[i][j]=1

def logic():
    # A function which decides the logic behind your move. Your bot's brain.
    # it passes arguements to the move function which updates


def move():
    logic()
    # function which to output the move made and update the grid


board_initialise()
turn = 0
turn = input()
inp = ""
while(True):
    if not turn==1:
        inp = raw_input()
        turn=1

    print move()      # output the move returned by the function




"""
Board representation:

X X X X X X
O _ _ _ _ X
O _ _ _ _ X
O _ _ _ _ X
O _ _ _ _ X
O _ _ _ _ X
O _ _ _ _ X
O O O O O O

X : player 1 token
O : player 2 token


Code representation:

6       0
1       1
1       1
1       1
1       1
1       1
1       1
1       1
0       6

each of the coloums represent the count of tokens a play has in that particular row.
"""
