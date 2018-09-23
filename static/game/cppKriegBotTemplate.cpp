#include<iostream>
#include<string.h>
using namespace std;

char board[5][5];
class move	//class for denoting a move
{
public:
	int x1,y1,x2,y2;
	move()	//constructor
	{
		x1=0;	y1=0;
		x2=0;	y2=0;
	}
    move(const move &tocopy)	//copy constructor
    {
        x1=tocopy.x1;	y1=tocopy.y1;
        x2=tocopy.x2;	y2=tocopy.y2;
    }
};
bool whoAmI;	//if whoAm = 1, you are Sentinels
				//if whoAm = 0, you are Scourges

//FUNCTIONS:
move findBestMove();	//returns the move you want to make
int mValidation();		//validates your sample move according to the given rules in the documentation
void makemove ();		//makes move temporarily
void undoMove();		//undoes the temporarily made move
int algorithm();		//your game's algorithm
int evaluate();			//evaluation for your move


void initBoard ()
{
    for (int i = 0; i < 5; i++)	// Initialize the Board
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
	bool turn;
	string input, output;
	cin>>turn;
	//if turn = 1, you are Sentinels and it's your turn first
	//if turn = 0, you are Scourges and it's opponent's turn first
	whoAmI=turn;


	while(1)
	{
		if(turn!=1)
		{
			getline(cin,input);
			//Input from opponent
			//Use this input to make changes in your board

			turn=0;	//after first iteration, (turn!=1) is always true
					//i.e. turn is always 0
		}

		//your logic to make the next move
		//output your move string
		cout<<output<<endl;
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

