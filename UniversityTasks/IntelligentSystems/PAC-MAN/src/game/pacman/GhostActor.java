package game.pacman;

import java.lang.Error;
import java.awt.*;

public class GhostActor {
    public final int IN=0;
    public final int OUT=1;
	public final int BLIND=2;
    public final int EYE=3;

    private boolean isPassMovement = false;

	final int[] steps=	{7, 7, 1, 1};
	final int[] frames=	{8, 8, 2, 1};

	final int INIT_BLIND_COUNT=600;	// remain blind for ??? frames
	int blindCount;

	PacManSpeed speed=new PacManSpeed();

	int myX, myY, myDir, myState;
	int myBlink, currentBlindCount;

	// random calculation factors
	final int DIR_FACTOR=2;
	final int POS_FACTOR=10;

	// the applet this object is associated to
	Window applet;
	Graphics graphics;

	// the maze the ghostActors knows
	Maze maze;

	// the ghost image
	Image imageGhost;
	Image imageBlind;
	Image imageEye;

	GhostActor(Window a, Graphics g, Maze m, Color color) {
		applet=a;
		graphics=g;
		maze=m;

		imageGhost=applet.createImage(18,18);
		ImageData.drawGhost(imageGhost, 0, color);

		imageBlind=applet.createImage(18,18);
		ImageData.drawGhost(imageBlind,1, Color.white);

		imageEye=applet.createImage(18,18);
		ImageData.drawGhost(imageEye,2, Color.lightGray);
	}

	public void start(int initialPosition, int round) {
		if (initialPosition>=2)
			initialPosition++;
		myX =(8+initialPosition)*16; myY =8*16;
		myDir =3;
		myState =IN;

		blindCount=INIT_BLIND_COUNT/((round+1)/2);

		speed.start(steps[myState], frames[myState]);
	}

	public void draw() {
		maze.DrawDot(myX /16, myY /16);
		maze.DrawDot(myX /16+(myX %16>0?1:0), myY /16+(myY %16>0?1:0));

		if (myState ==BLIND && myBlink ==1 && currentBlindCount %32<16)
			graphics.drawImage(imageGhost, myX -1, myY -1, applet);
		else if (myState ==OUT || myState ==IN)
			graphics.drawImage(imageGhost, myX -1, myY -1, applet);
		else if (myState ==BLIND)
			graphics.drawImage(imageBlind, myX -1, myY -1, applet);
		else
			graphics.drawImage(imageEye, myX -1, myY -1, applet);
	}

	//	public void get () {return;}
	//	public void get () {return;}
	public int getMyState() {return myState;}
	public void setMyState(int value) { myState = value;}

	public int getCurrentBlindCount() {return currentBlindCount;}
	public void setCurrentBlindCount(int value) { currentBlindCount = value;}

    public int getBlindCount() {return blindCount;}
    public void setBlindCount(int value) { blindCount = value;}

    public int getMyBlink() {return myBlink;}
    public void setMyBlink(int value) { myBlink = value;}

    public boolean getIsPassMovement() {return isPassMovement;}
    public void setIsPassMovement(boolean value) { isPassMovement = value;}

    public int getIsMove() {return speed.isMove();}

    public int getMyX() {return myX;}
    public void setMyX(int value) { myX = value;}

    public int getMyY() {return myY;}
    public void setMyY(int value) { myY = value;}

    public void setMyDir(int value) { myDir = value;}
    public int getMyDir() {return myDir;}

	public int INSelect() throws Error {
		int iM,i,iRand;
		int iDirTotal=0;

		for (i=0; i<4; i++)
		{
			iM=maze.iMaze[myY /16 + DirectionMap.YDirection[i]]
					[myX /16 + DirectionMap.XDirection[i]];
			if (iM!= Maze.WALL && i != DirectionMap.iBack[myDir] )
			{
				iDirTotal++;
			}
		}
		// randomly select a direction
		if (iDirTotal!=0)
		{
			iRand= RandomUtils.RandSelect(iDirTotal);
			if (iRand>=iDirTotal)
				throw new Error("iRand out of range");
			//				exit(2);
			for (i=0; i<4; i++)
			{
				iM=maze.iMaze[myY /16+ DirectionMap.YDirection[i]]
						[myX /16+ DirectionMap.XDirection[i]];
				if (iM!= Maze.WALL && i != DirectionMap.iBack[myDir] )
				{
					iRand--;
					if (iRand<0)
					// the right selection
					{
						if (iM== Maze.DOOR)
							myState =OUT;
						myDir =i;	break;
					}
				}
			}
		}
		return(myDir);
	}

	public int OUTSelect(int iPacX, int iPacY, int iPacDir) throws Error {
		int iM,i,iRand;
		int iDirTotal=0;
		int[] iDirCount=new int [4];

		for (i=0; i<4; i++) {
			iDirCount[i]=0;
			iM=maze.iMaze[myY /16 + DirectionMap.YDirection[i]]
					[myX /16+ DirectionMap.XDirection[i]];
			if (iM!= Maze.WALL && i!= DirectionMap.iBack[myDir] && iM!= Maze.DOOR ) {
				iDirCount[i]++;
				iDirCount[i]+= myDir ==iPacDir?
						DIR_FACTOR:0;
				switch (i) {
					case 0:	// right
						iDirCount[i] += iPacX > myX ? POS_FACTOR:0;
						break;
					case 1:	// up
						iDirCount[i]+=iPacY< myY ?
								POS_FACTOR:0;
						break;
					case 2:	// left
						iDirCount[i]+=iPacX< myX ?
								POS_FACTOR:0;
						break;
					case 3:	// down
						iDirCount[i]+=iPacY> myY ?
								POS_FACTOR:0;
						break;
				}
				iDirTotal+=iDirCount[i];
			}
		}
		// randomly select a direction
		if (iDirTotal!=0) {
			iRand= RandomUtils.RandSelect(iDirTotal);
			if (iRand>=iDirTotal)
				throw new Error("iRand out of range");
			// exit(2);
			for (i=0; i<4; i++)
			{
				iM=maze.iMaze[myY /16+ DirectionMap.YDirection[i]]
						[myX /16+ DirectionMap.XDirection[i]];
				if (iM!= Maze.WALL && i!= DirectionMap.iBack[myDir] && iM!= Maze.DOOR )
				{
					iRand-=iDirCount[i];
					if (iRand<0)
					// the right selection
					{
						myDir =i;	break;
					}
				}
			}
		}
		else
			throw new Error("iDirTotal out of range");
		// exit(1);
		return(myDir);
	}

	public void blind() {
		if (myState ==BLIND || myState ==OUT) {
			myState =BLIND;
			currentBlindCount =blindCount;
			myBlink =0;
			// reverse
			if (myX %16!=0 || myY %16!=0) {
				myDir = DirectionMap.iBack[myDir];
				// a special condition:
				// when ghost is leaving home, it can not go back
				// while becoming blind
				int iM;
				iM=maze.iMaze[myY /16+ DirectionMap.YDirection[myDir]]
						[myX /16+ DirectionMap.XDirection[myDir]];
				if (iM == Maze.DOOR)
					myDir = DirectionMap.iBack[myDir];
			}
		}
	}

	public int EYESelect() throws Error {
		int iM,i,iRand;
		int iDirTotal=0;
		int [] iDirCount= new int [4];

		for (i=0; i<4; i++) {
			iDirCount[i]=0;
			iM=maze.iMaze[myY /16 + DirectionMap.YDirection[i]]
					[myX /16+ DirectionMap.XDirection[i]];
			if (iM!= Maze.WALL && i!= DirectionMap.iBack[myDir]) {
				iDirCount[i]++;
				switch (i) {
					// door position 10,6
					case 0:	// right
						iDirCount[i]+=160> myX ?
								POS_FACTOR:0;
						break;
					case 1:	// up
						iDirCount[i]+=96< myY ?
								POS_FACTOR:0;
						break;
					case 2:	// left
						iDirCount[i]+=160< myX ?
								POS_FACTOR:0;
						break;
					case 3:	// down
						iDirCount[i]+=96> myY ?
								POS_FACTOR:0;
						break;
				}
				iDirTotal+=iDirCount[i];
			}
		}
		// randomly select a direction
		if (iDirTotal!=0) {
			iRand= RandomUtils.RandSelect(iDirTotal);
			if (iRand>=iDirTotal)
				throw new Error("RandSelect out of range");
			for (i=0; i<4; i++) {
				iM=maze.iMaze[myY /16+ DirectionMap.YDirection[i]]
						[myX /16+ DirectionMap.XDirection[i]];
				if (iM!= Maze.WALL && i!= DirectionMap.iBack[myDir]) {
					iRand-=iDirCount[i];
					if (iRand<0) {
						if (iM== Maze.DOOR)
							myState =IN;
						myDir =i;	break;
					}
				}
			}
		}
		else
			throw new Error("iDirTotal out of range");
		return(myDir);
	}

	public int BLINDSelect(int iPacX, int iPacY, int iPacDir) throws Error {
		int iM,i,iRand;
		int iDirTotal=0;
		int [] iDirCount = new int [4];

		for (i=0; i<4; i++) {
			iDirCount[i]=0;
			iM=maze.iMaze[myY /16+ DirectionMap.YDirection[i]][myX /16+ DirectionMap.XDirection[i]];
			if (iM != Maze.WALL && i != DirectionMap.iBack[myDir] && iM != Maze.DOOR) {
				iDirCount[i]++;
				iDirCount[i]+= myDir ==iPacDir?
						DIR_FACTOR:0;
				switch (i) {
					case 0:	// right
						iDirCount[i]+=iPacX< myX ?
								POS_FACTOR:0;
						break;
					case 1:	// up
						iDirCount[i]+=iPacY> myY ?
								POS_FACTOR:0;
						break;
					case 2:	// left
						iDirCount[i]+=iPacX> myX ?
								POS_FACTOR:0;
						break;
					case 3:	// down
						iDirCount[i]+=iPacY< myY ?
								POS_FACTOR:0;
						break;
				}
				iDirTotal+=iDirCount[i];
			}
		}
		// randomly select a direction
		if (iDirTotal!=0) {
			iRand= RandomUtils.RandSelect(iDirTotal);
			if (iRand>=iDirTotal)
				throw new Error("RandSelect out of range");
			for (i=0; i<4; i++) {
				iM=maze.iMaze[myY /16+ DirectionMap.YDirection[i]]
						[myX /16+ DirectionMap.XDirection[i]];
				if (iM!= Maze.WALL && i!= DirectionMap.iBack[myDir]) {
					iRand-=iDirCount[i];
					if (iRand<0) {
						myDir =i;	break;
					}
				}
			}
		}
		else throw new Error("iDirTotal out of range");
		return(myDir);
	}

	int testCollision(int iPacX, int iPacY) {
		if (myX <=iPacX+2 && myX >=iPacX-2
				&& myY <=iPacY+2 && myY >=iPacY-2) {
			switch (myState) {
				case OUT:
					return(1);
				case BLIND:
					myState =EYE;
					myX = myX /4*4;
					myY = myY /4*4;
					return(2);
			}
		}
		// nothing
		return(0);
	}
}
