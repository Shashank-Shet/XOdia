#include<stdio.h>
int board[8][2]; // board dimension in code


void initialize()        //function to initialize the board  
{   
  board[8][2];
  board[0][0] = 6;
  board[7][1] = 6;
  for(int i =1; i<7 ; i++)
    {
      for(int j=0;j<2;j++)
	board[i][j] = 1;
    }  
}

int main()
{
  int turn;
  scanf("%d", &turn);
  char x[8], y[8];  
  while(1)
    {
	
      if (!(turn==1))
	{
	  scanf("%s", x);
	  turn=1;
	}
      //input scanned by the player for every iteration specifying the opponent’s previous move: X

      //player's logic
		

      printf("%s\n", y);
      //output printed by the player at the end of every iteration specifying the current move: Y
      //NOTE: The trailing '\n' character is necessary.
    }
}
/*	                     
xi= 1 || xi= 2
x={ “i1,f1,i2,f2” | 0 <= i1,f1,i2,f2 <= 7 }
y={ “i1,f1,i2,f2” | 0 <= i1,f1,i2,f2 <= 7 }

your code should output a string of length 7 which contains 4 integers each seperated by a comma as: i1,f1,i2,f2 where i1 and f1 are the initial and final indices of rows for first attack. Similarly i2 and f2 are initial and final indices of rows for second attack.
                     
Board representation:              

X X X X X X
X _ _ _ _ O
X _ _ _ _ O
X _ _ _ _ O        
X _ _ _ _ O        
X _ _ _ _ O
X _ _ _ _ O
O O O O O O

X : player 1 token
O: player 2 token


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

each of the columns represent the count of tokens a player has in that particular row.

*/     
