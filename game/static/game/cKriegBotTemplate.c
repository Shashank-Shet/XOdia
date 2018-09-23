#include <stdio.h>
#include<string.h>

char board[5][5];	//Your board

struct move		//structure for denoting a move
{
	int x1,y1,x2,y2;
};

int whoAmI;		//if whoAmI = 1, you are Sentinels
				//if whoAmI = 0, you are Scourges

//FUNCTIONS:
struct move findBestMove();	//returns the move you want to make
int mValidation();		//validates your sample move according to the given rules in the documentation
void makemove ();		//makes move temporarily
void undoMove();		//undoes the temporarily made move
int algorithm();		//your game's algorithm
int evaluate();			//evaluation for your move

void initBoard ()		//Function to initialize the Board
{
    for (int i = 0; i < 5; i++)
    {
        board[0][i] = 'B';
        board[1][i] = 'b';
        board[2][i] = '_';
        board[3][i] = 'r';
        board[4][i] = 'R';
    }
}

int main()
{
	initBoard();
	int turn;
	char input[8], output[8];
	scanf("%d", &turn);
	//if turn = 1, you are Sentinels and it's your turn first
	//if turn = 0, you are Scourges and it's opponent's turn first
	whoAmI=turn;


	while(1)
	{
		if(turn!=1)
		{
			fgets(input, 8, stdin);
			//Input from opponent
			//Use this input to make changes in your board

			turn=0;	//after first iteration, (turn!=1) is always true
					//i.e. turn is always 0
		}

		//your logic to make the next move
		//output your move string
		printf("%s\n", output);
	}
}

/*
 * x = {"x1 y1 x2 y2"}
 * y = {"x1 y1 x1 y2"}
 *
 * Your code outputs a string of length 7 containing 4 characters each
 * separated by a space, where x1 & y1 are respective row and column
 * of your piece's initial position and x2 & y2 are respective row and
 * column of your piece's final position.
 *
 * Each of x1,y1,x2,y2 must be >=0 and <5.
 *
 * Consider "B"-> Sentinels' bombers "b"-> Sentinels' stingers
 * 			"R"-> Scourges' bombers "r"-> Scourges' stingers
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
 */

