package game.pacman;

import java.awt.*;

public class PacManActor {
	// frames to wait after eaten a dot
	final int DOT_WAIT=4;

	int iDotWait;

	// current position
	int myX, myY;
	// current direction
	int myDir;

	public int getMyX() {return myX;}
	public int getMyY() {return myY;}
	public int getMyDir() { return myDir;}

	// the applet this object is associated to
	Window applet;
	Graphics graphics;

	// the pac image
	Image [][] imagePac;

	// the knowledge of the maze
	Maze maze;

	// the knowledge of the power dots
	PacManEat powerDot;

	//    PacManMove cAuto;

	//  PacManActor(Window a, Graphics g, Maze m, PacManEat p, GhostActor GhostActor[])
	PacManActor(Window a, Graphics g, Maze m, PacManEat p) {
		applet=a;
		graphics=g;
		maze=m;
		powerDot=p;

		//      cAuto=new PacManMove(this, GhostActor, m);

		// initialize pac and pac image
		imagePac=new Image[4][4];
		for (int i=0; i<4; i++)
			for (int j=0; j<4; j++)
			{
				imagePac[i][j]=applet.createImage(18,18);
				ImageData.drawPac(imagePac[i][j],i,j);
			}	
	}

	public void start() {
		myX =10*16;
		myY =10*16;
		myDir =1;		// downward, illegal and won't move
		iDotWait=0;
	}

	public void draw() {
		maze.DrawDot(myX /16, myY /16);
		maze.DrawDot(myX /16+(myX %16>0?1:0), myY /16+(myY %16>0?1:0));

		int iImageStep=(myX %16 + myY %16)/2; 	// determine shape of PAc
		if (iImageStep<4)
			iImageStep=3-iImageStep;
		else
			iImageStep-=4;
		graphics.drawImage(imagePac[myDir][iImageStep], myX -1, myY -1, applet);
	}	

	public int move(int iNextDir) {
		int eaten=0;

		//      iNextDir=cAuto.GetNextDir();

		if (iNextDir!=-1 && iNextDir!= myDir)	// not set or same
			// change direction
		{
			if (myX %16!=0 || myY %16!=0)
			{
				// only check go back
				if (iNextDir%2== myDir %2)
					myDir =iNextDir;
			}	
			else    // need to see whether ahead block is OK
			{
				if ( mazeOK(myX /16+ DirectionMap.XDirection[iNextDir],
						myY /16+ DirectionMap.YDirection[iNextDir]) )
				{
					myDir =iNextDir;
					iNextDir=-1;
				}
			}
		}
		if (myX %16==0 && myY %16==0)
		{

			// see whether has eaten something
			switch (maze.iMaze[myY /16][myX /16])
			{
			case Maze.DOT:
				eaten=1;
				maze.iMaze[myY /16][myX /16]= Maze.BLANK;	// eat dot
				maze.iTotalDotcount--;
				iDotWait=DOT_WAIT;
				break;
			case Maze.POWER_DOT:
				eaten=2;
				powerDot.eat(myX /16, myY /16);
				maze.iMaze[myY /16][myX /16]= Maze.BLANK;
				break;
			}

			if (maze.iMaze[myY /16+ DirectionMap.YDirection[myDir]]
			               [myX /16+ DirectionMap.XDirection[myDir]]==1)
			{
				return(eaten);	// not valid move
			}
		}
		if (iDotWait==0)
		{
			myX += DirectionMap.XDirection[myDir];
			myY += DirectionMap.YDirection[myDir];
		}
		else	iDotWait--;
		return(eaten);
	}	

	boolean mazeOK(int iRow, int icol) {
		if ( (maze.iMaze[icol][iRow] & ( Maze.WALL | Maze.DOOR)) ==0)
			return(true);
		return(false);
	}
}









