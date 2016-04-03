package game.pacman;

class PacManMove {
	int myDirScore[];

	int myDirValid[];

	PacManActor cPac;
	GhostActor[] cGhostActor;
	Maze cMaze;

	PacManMove(PacManActor pac, GhostActor ghostActor[], Maze maze) {
		myDirScore =new int[4];

		myDirValid =new int [4];
		cPac=pac;

		cGhostActor =new GhostActor[4];
		for (int i=0; i<4; i++)
			cGhostActor[i]= ghostActor[i];

		cMaze=maze;
	}

	public int GetNextDir() throws Error {
		int i;

		// first, init to 0
		for (i=0; i<4; i++)
			myDirScore[i]=0;

		// add currentScore for dot
		AddDotScore();

		// add currentScore for ghostActors
		AddGhostScore();

		// add currentScore for powerdot
		AddPowerDotScore();

		// determine the direction based on scores

		for (i=0; i<4; i++)
			myDirValid[i]=1;

		int iHigh, iHDir;

		while (true) 
		{
			iHigh=-1000000;
			iHDir=-1;
			for (i=0; i<4; i++)
			{
				if (myDirValid[i] == 1 && myDirScore[i]>iHigh)
				{
					iHDir=i;
					iHigh= myDirScore[i];
				}
			}

			if (iHDir == -1)
			{
				throw new Error("PacManMove: can't find a way?");
			}

			if ( cPac.myX %16 == 0 && cPac.myY %16==0)
			{
				if ( cPac.mazeOK(cPac.myX /16 + DirectionMap.XDirection[iHDir],
						cPac.myY /16 + DirectionMap.YDirection[iHDir]) )
					return(iHDir);
			}
			else
				return(iHDir);

			myDirValid[iHDir]=0;
			//			myDirScore[DirectionMap.iBack[iHDir]] = myDirScore[iHDir];

		}

		//	return(iHDir);  // will not reach here, ordered by javac
	}

	void AddGhostScore() {
		int iXDis, iYDis;	// distance
		double iDis;		// distance

		int iXFact, iYFact;

		// calculate ghostActors one by one
		for (int i=0; i<4; i++)
		{
			iXDis= cGhostActor[i].myX - cPac.myX;
			iYDis= cGhostActor[i].myY - cPac.myY;

			iDis=Math.sqrt(iXDis*iXDis+iYDis*iYDis);

			if (cGhostActor[i].myState == cGhostActor[i].BLIND)
			{


			}
			else
			{
				// adjust iDis into decision factor

				iDis=18*13/iDis/iDis;
				iXFact=(int)(iDis*iXDis);
				iYFact=(int)(iDis*iYDis);

				if (iXDis >= 0)
				{
					myDirScore[DirectionMap.LEFT] += iXFact;
				}
				else
				{
					myDirScore[DirectionMap.RIGHT] += -iXFact;
				}

				if (iYDis >= 0)
				{
					myDirScore[DirectionMap.UP] += iYFact;
				}
				else
				{
					myDirScore[DirectionMap.DOWN] += -iYFact;
				}
			}
		}
	}

	void AddDotScore() {
		int i, j;

		int dDis, dShortest;
		int iXDis, iYDis;
		int iX=0, iY=0;

		dShortest=1000;

		// find the nearest dot
		for (i=0; i < Maze.HEIGHT; i++)
			for (j=0; j < Maze.WIDTH; j++)
			{
				if (cMaze.iMaze[i][j]== Maze.DOT)
				{
					iXDis=j*16-8-cPac.myX;
					iYDis=i*16-8-cPac.myY;
					dDis=iXDis*iXDis+iYDis*iYDis;

					if (dDis<dShortest)
					{
						dShortest=dDis;

						iX=iXDis; iY=iYDis;
					}
				}	
			}

		// now myX and myY is the goal (relative position)

		int iFact=100000;

		if (iX > 0)
		{
			myDirScore[DirectionMap.RIGHT] += iFact;
		}
		else if (iX < 0)
		{
			myDirScore[DirectionMap.LEFT] += iFact;
		}

		if (iY > 0)
		{
			myDirScore[DirectionMap.DOWN] += iFact;
		}
		else if (iY<0)
		{
			myDirScore[DirectionMap.UP] += iFact;
		}
	}

	void AddPowerDotScore() { }
}
