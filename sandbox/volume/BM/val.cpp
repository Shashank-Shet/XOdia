#include <iostream>
#include <string.h>
using namespace std;
char board[5][5];/*=
    {		//use this for testing otherwise initBoard is called in main

        {'_', '_', '_', '_', '_'},
        {'_', 'W', '_', '_', '_'},
        {'_', 'b', 'W', 'W', '_'},
        {'_', '_', '_', 'B', 'b'},
        {'_', 'b', 'b', 'b', 'b'},

    };*/
int flag = 0, Wm = 0, Wp = 0, Bm = 0, Bp = 0;

bool whosemove = 1;
int result;
int sum1 = 0, sum2 = 0, goFlag=0, finale = 0;		//goFlag-> gameoverFlag to check if the mValidation is for gameover()
char X, Y;
string s;

class game
{
public:
	int r, c;
};
int move();
int mValidation (game, game);
void Elimination (game, game);
void elim_package (game, game, int, int, int);	//it's called from mValidation
int checkVerticalElimination (game, game);
int checkHorizontalElimination (game, game, int);
void colour_generalize (int);
void makeMove (game, game);
void displayboard ();
int gameover ();
void winner();

int gameover ()
{
	if(Bm==5)
	{
		cout<<"WIN\n";
		cout<<s<<endl;
		cout<<"0"<<endl;
		cout<<"All Bombers Eliminated"<<endl;

		return 1;
	}
	else if(Wm==5)
	{
		cout<<"WIN\n";
		cout<<s<<endl;
		cout<<"1"<<endl;
		cout<<"All Bombers Eliminated"<<endl;

		return 1;
	}

    bool x = whosemove;
    colour_generalize (x);
    char X1=X;
    char Y1=Y;

    game gsinput, gminput;
    int i, j, k, l;

    for (j = 0; j < 5; j++)
    {
        if (board[0][j] == 'W')
    	{
    		cout<<"WIN\n";
    		cout<<s<<endl;
    		cout<<"0"<<endl;
    		cout<<"Bomber Reached Home"<<endl;

    		return 1;
    	}
        if (board[4][j] == 'B')
        {
			cout<<"WIN\n";
			cout<<s<<endl;
			cout<<"1"<<endl;
			cout<<"Bomber Reached Home"<<endl;

			return 1;
		}
    }

	for (i = 0; i < 5; i++)
	{
		for (j = 0; j < 5; j++)
		{
			if (board[i][j] == '_')	//if place on board is blank then continue
			{
				continue;
			}
			else if (board[i][j] == X1 || board[i][j] == Y1)
			{
				gsinput.r = i;
				gsinput.c = j;
				for (k = 0; k<=2; k++)
				{
					for (l = -2; l <= 2; l++)
					{
						if(x==1)
						{gminput.r = i + k;}
						else
						{gminput.r = i - k;}
						gminput.c = j + l;
						if (gminput.c <= 4 && gminput.c >= 0 && gminput.r <= 4 && gminput.r >= 0)
						{
							goFlag = mValidation (gsinput, gminput);
							if (goFlag == 1 || goFlag == 2)
							{
								return 0;	//still valid moves left
							}
						}
					}
				}
			}
		}
	}

    return 2;
}

void winner()
{
	if(Wm>Bm)
	{
		cout<<"WIN\n";
		cout<<s<<endl;
		cout<<"0"<<endl;
		cout<<"NO MOVES LEFT, 0 HAS MORE BOMBERS LEFT"<<endl;
	}
	else if(Bm>Wm)
	{
		cout<<"WIN\n";
		cout<<s<<endl;
		cout<<"1"<<endl;
		cout<<"NO MOVES LEFT, 1 HAS MORE BOMBERS LEFT"<<endl;

	}
	else if(Wm==Bm)
	{
		if(Wp>Bp)
		{
			cout<<"WIN\n";
			cout<<s<<endl;
			cout<<"0"<<endl;
			cout<<"NO MOVES LEFT, 0 HAS MORE STINGERS LEFT"<<endl;
		}
		else if(Bp>Wp)
		{
			cout<<"WIN\n";
			cout<<s<<endl;
			cout<<"1"<<endl;
			cout<<"NO MOVES LEFT, 1 HAS MORE STINGERS LEFT"<<endl;
		}
		else
		{
			cout<<"DRAW\n";
			cout<<s<<endl;
			cout<<whosemove<<endl;
		}
	}
}
int mValidation (game sinput, game minput)
{
    int d1, d2, x = whosemove;
    d1 = minput.r - sinput.r;	// difference between initial and final row position
    d2 = minput.c - sinput.c;	//difference between initial and final cols position
    colour_generalize (x);	//generalize all functions to work for either colour
    if (board[minput.r][minput.c] == '_' && minput.c >= 0 && minput.c <= 4 && minput.r <= 4 && minput.c >= 0)	//check if final position is vacant
    {
        if (board[sinput.r][sinput.c] == X)	//moveset for mantri
	    {
	        if ((d1 == (2 * x - 1) || d1 == 0) && (d2 == (2 * x - 1) || d2 == -(2 * x - 1) || d2 == 0))	//mantri moves single space in any allowed direction
	        {
	            flag = 1;		//signifies valid non-eliminating move,turn passes to opponent
	        }
	        else if ((d1 == 2 * (2 * x - 1) && d2 == 0) || (d1 == 0 && (d2 == 2 * (2 * x - 1) || d2 == -2 * (2 * x - 1))))	//moves two spaces, in an elimination move
	        {
	            elim_package (sinput, minput, x, d1, d2);	//checks if elimination is possible and sets flag accordingly
	        }
	        else
	        {
	            flag = 0;
	        }
	    }
        else if (board[sinput.r][sinput.c] == Y)	//moveset for pawn
	    {
	        if ((d1 == (2 * x - 1) && d2 == (2 * x - 1)) || (d1 == (2 * x - 1) && d2 == -(2 * x - 1)))	//moves a single space
	        {
	            flag = 1;
	        }
	        else if ((d1 == 2 * (2 * x - 1) && d2 == 0) || (d1 == 0 && (d2 == 2 * (2 * x - 1) || d2 == -2 * (2 * x - 1))))	//moves two spaces, in an elimination move
	        {
	            elim_package (sinput, minput, x, d1, d2);
	        }
	        else
	        {
	            flag = 0;
	        }
	    }
    }
    else
    {
        flag = 0;
    }
    return flag;
}

void elim_package (game sinput, game minput, int x, int d1, int d2)
{
    if (d1 == 2 * (2 * x - 1) && d2 == 0)	//mantri moves two rows up, in an elimination move
    {
        flag = checkVerticalElimination (sinput, minput);	//call function that checks conditions for eliminations
    }
    else if (d1 == 0 && (d2 == 2 * (2 * x - 1) || d2 == -2 * (2 * x - 1)))	//mantri moves horizontally in elimination move
    {
        flag = checkHorizontalElimination (sinput, minput, x);
    }

}

int checkVerticalElimination (game sinput, game minput)
{
    bool x = whosemove;
    char t1 = board[(sinput.r + minput.r) / 2][(sinput.c + minput.c) / 2];	//target piece  //changing value of X and Y temporarily to detect correct target
    colour_generalize (!x);
    if ((t1 == X || t1 == Y))	//check if neighbouring squares and piece being attacked
    {
        return 2;
    }
    else
    {
        return 0;
    }
}

int checkHorizontalElimination (game sinput, game minput, int x)
{
    char t1 = board[(sinput.r + minput.r) / 2][(sinput.c + minput.c) / 2];
    colour_generalize (!x);	//changing value of X and Y temporarily to detect correct target
    if ((t1 == X || t1 == Y)&& sinput.r!=4 && sinput.r!=0)	//check if neighbouring squares and piece being attacked
    {
        return 2;
    }
    else
    {
        return 0;
    }
}
void Elimination (game sinput, game minput)
{
    bool x=!whosemove;
    colour_generalize(x);
    char t1 = board[(sinput.r + minput.r) / 2][(sinput.c + minput.c) / 2];
    if(x==1)
    {
        if (t1 == X)
        {
        	Bm++;			//increment count for dead mantri
        }
        else
        {
            Bp++;			//increment count for dead pawn
        }
    }
    else
    {
         if (t1 == X)
	    {
	        Wm++;			//increment count for dead mantri
        }
        else
	    {
            Wp++;			//increment count for dead pawn
	    }
    }
    board[(sinput.r + minput.r) / 2][(sinput.c + minput.c) / 2] = '_';
}

int move ()
{
	flag=0;
	
    game sinput, minput;
    int lengths;

    int x = whosemove;
    colour_generalize (x);
    //cout << "Enter Input\n";
    getline(cin,s);
    lengths=s.size();
    if(lengths==7)
    {
        for(int i=1;i<lengths;i++)
        {
        	if(s[i]!=' ')
        	{
        		cout<<"INVALID INPUT\n";
        		return 0;
        	}
        	i++;
        }
        for(int i=0;i<lengths;i++)
        {
        	if((s[i]<48 || s[i]>54))
        	{
        		cout<<"INVALID INPUT\n";
        		return 0;
        	}
        	i++;
        }

        sinput.r = s[0]-48;
        sinput.c = s[2]-48;
        minput.r = s[4]-48;
        minput.c = s[6]-48;
        if (board[sinput.r][sinput.c] == X || board[sinput.r][sinput.c] == Y)
        {
        	flag = mValidation (sinput, minput);	//to check if the selected move is valid
        	if (flag == 1 || flag == 2)	// 1->non eliminating move 2->eliminating move
        	{
        		makeMove(sinput,minput);
        	}
        	else if (flag == 0)
        	{
        		cout << "INVALID MOVE\n";
        		return 0;
        	}
        }
        else
        {
        	cout << "INVALID PIECE SELECTION\n";
        	return 0;
        }
    }
    else
    {
    	cout<<"INVALID INPUT STRING LENGTH\n";
    	return 0;
    }
    return 1;
}
void makeMove (game sinput, game minput)
{
    if (flag == 1)
    {
        board[minput.r][minput.c] = board[sinput.r][sinput.c];
        board[sinput.r][sinput.c] = '_';
    }
    else if (flag == 2)
    {
        board[minput.r][minput.c] = board[sinput.r][sinput.c];
        board[sinput.r][sinput.c] = '_';
        Elimination (sinput, minput);
    }
}

void colour_generalize (int x)
{
    if (x == 0)
    {
        X = 'W';			//X initialized to mantri
        Y = 'w';			//Y initialized to pawn
    }
    else
    {
        X = 'B';
        Y = 'b';
    }
}

void displayboard ()
{
    int i, j;
    cout << "    0 1 2 3 4\n";
    cout << "  -----------\n";
    for (i = 0; i < 5; i++)
    {
        cout << i << "|  ";
        for (j = 0; j < 5; j++)
	    {
	        cout << board[i][j] << ' ';
	    }
        cout << "\n";
    }
}

void initBoard ()
{
    for (int i = 0; i < 5; i++)	// Initialize the Board
    {
        board[0][i] = 'B';
        board[1][i] = 'b';
        board[2][i] = '_';
        board[3][i] = 'w';
        board[4][i] = 'W';
    }
}
int main ()
{
    	initBoard();
	int moveOutput=1;
	int gameOverOutput=0;
	while(moveOutput && gameOverOutput==0)
	{
		int moveOutput=move();	//moveOutput=0(i.e.errors) is handled in move() itself
		//finale=gameover();

		if(moveOutput==1)
		{

			int gameOverOutput=gameover();	//gameOverOutput=1 is handled in gameover() itself
			if(gameOverOutput==0)
			{
				cout<<"VALID\n";
				cout<<s<<endl;	//returns the move as it is
			}
			else if(gameOverOutput==2)
			{
				winner();
			}
			
		}
		whosemove=!whosemove;
	
	}//finale==0);

	return 0;
}
