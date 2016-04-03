package game.pacman;

import org.drools.KnowledgeBase;
import org.drools.KnowledgeBaseFactory;
import org.drools.builder.*;
import org.drools.io.ResourceFactory;
import org.drools.runtime.StatefulKnowledgeSession;

import java.awt.*;
import java.awt.event.*;

public class PacManGame extends Frame implements Runnable, KeyListener, WindowListener {

	private final int INIT_IMAGE = 100;
	private final int START_WAIT = 0;
	private final int RUNNING = 1;
	private final int DEAD_WAIT = 2;
    private final int SUSPENDED=3;

    private final int NONE=0;
    private final int SUSPEND=1;
    private final int BOSS=2;

    private int gameState;

	private final int WAIT_COUNT = 90;


	private final ThreadLocal<Thread> timer = new ThreadLocal<>();
	private final ThreadLocal<Image> offScreen = new ThreadLocal<>();
	private final ThreadLocal<Graphics> offScreenG = new ThreadLocal<>();
	private final ThreadLocal<Maze> maze = new ThreadLocal<>();

	private PacManEat powerDot;

    private PacManActor pac;
    private GhostActor[] ghostActors;

    private Image imgScore;
    private Graphics imgScoreG;
    private Image imgHiScore;
    private Graphics imgHiScoreG;

    private KnowledgeBase kBase;

	private int timerPeriod=12;

	private int signalMove=0;

    private int pacmanKeyDir;
    private int key=0;

	private final int canvasWidth = 23*16;
	private final int canvasHeight = 18*16;

    private int topOffset;
    private int leftOffset;

    private final int marginMazeX = 16;
    private final int marginMazeY = 16;

    private final int pacmanLives = 3;
    private int pacRemain;
    private int changePacRemain;

    private int currentScore;
    private int hiScore;
    private int ghostScore;
    private int changeScore;
    private int changeHiScore;

    private int wait;

    private int round;

    private boolean newMaze;

    private boolean finalized=false;

    public PacManGame() {
		super("PAC-MAN Intelligent");

		hiScore=0;

		gameState= INIT_IMAGE;

		addWindowListener(this);

		addKeyListener(this);

        // set the proper size of canvas
        Insets insets=getInsets();

        topOffset=insets.top+insets.bottom;
        leftOffset=0;

        int ScreenWidth = Toolkit.getDefaultToolkit().getScreenSize().width;
        int ScreenHeight = Toolkit.getDefaultToolkit().getScreenSize().height;

        setLocation( (ScreenWidth - canvasWidth)/2, (ScreenHeight - canvasHeight)/2);

        setSize(canvasWidth+insets.left+insets.right,
					canvasHeight+topOffset);

        setResizable(true);
        show();

		KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
		kbuilder.add(ResourceFactory.newClassPathResource("main/resources/ghost.drl"), ResourceType.DRL);
		KnowledgeBuilderErrors errors = kbuilder.getErrors();
		if (errors.size() > 0) {
			for (KnowledgeBuilderError error: errors) {
				System.err.println(error);
			}
			throw new IllegalArgumentException("Could not parse knowledge.");
		}
        kBase = KnowledgeBaseFactory.newKnowledgeBase();
        kBase.addKnowledgePackages(kbuilder.getKnowledgePackages());



	}

	public void initImages() {
		// initialize off screen drawing canvas
		offScreen.set(createImage(Maze.iWidth, Maze.iHeight));
		if (offScreen.get() ==null)
			System.out.println("createImage failed");
		offScreenG.set(offScreen.get().getGraphics());

		// initialize maze object
		maze.set(new Maze(this, offScreenG.get()));

		// initialize ghostActors object
		// 4 ghostActors
		ghostActors = new GhostActor[4];
		for (int i=0; i<4; i++)
		{
			Color color;
			if (i==0)
				color=Color.red;
			else if (i==1)
				color=Color.blue;
			else if (i==2)
				color=Color.white;
			else
				color=Color.orange;
			ghostActors[i]=new GhostActor(this, offScreenG.get(), maze.get(), color);
		}

		// initialize power dot object
		powerDot = new PacManEat(this, offScreenG.get(), ghostActors);

		// initialize pac object
		//      	pac = new PacManActor(this, offScreenG, maze, powerDot, ghostActors);
		pac = new PacManActor(this, offScreenG.get(), maze.get(), powerDot);

		// initialize the currentScore images
		imgScore=createImage(150,16);
		imgScoreG=imgScore.getGraphics();
		imgHiScore=createImage(150,16);
		imgHiScoreG=imgHiScore.getGraphics();

		imgHiScoreG.setColor(Color.black);
		imgHiScoreG.fillRect(0,0,150,16);
		imgHiScoreG.setColor(Color.red);
		imgHiScoreG.setFont(new Font("Helvetica", Font.BOLD, 12));
		imgHiScoreG.drawString("HI SCORE", 0, 14);

		imgScoreG.setColor(Color.black);
		imgScoreG.fillRect(0,0,150,16);
		imgScoreG.setColor(Color.green);
		imgScoreG.setFont(new Font("Helvetica", Font.BOLD, 12));
		imgScoreG.drawString("SCORE", 0, 14);
	}

	void startTimer() {
		// start the timer
		timer.set(new Thread(this));
		timer.get().start();
	}

	void startGame() {
		pacRemain= pacmanLives;
		changePacRemain=1;

		currentScore =0;
		changeScore=1;

		newMaze=true;

		round=1;

		startRound();
	}

	void startRound() {
		// new round for maze?
		if (newMaze==true)
		{
			maze.get().start();
			powerDot.start();
			newMaze=false;
		}

		maze.get().draw();	// draw maze in off screen buffer

		pac.start();
		pacmanKeyDir = DirectionMap.DOWN;
		for (int i=0; i<4; i++)
			ghostActors[i].start(i,round);

		gameState= START_WAIT;
		wait= WAIT_COUNT;
	}

	public void paint(Graphics g) {
		if (gameState == INIT_IMAGE){
			initImages();
			startGame();
			startTimer();
		}

		g.setColor(Color.black);
		g.fillRect(leftOffset,topOffset,canvasWidth, canvasHeight);

		changeScore=1;
		changeHiScore=1;
		changePacRemain=1;

		paintUpdate(g);
	}

	void paintUpdate(Graphics g) {
		// updating the frame

		powerDot.draw();

		for (int i=0; i<4; i++)
			ghostActors[i].draw();

		pac.draw();

		// display the offscreen
		g.drawImage(offScreen.get(),
				marginMazeX + leftOffset, marginMazeY + topOffset, this);

		// display extra information
		if (changeHiScore==1)
		{
			imgHiScoreG.setColor(Color.black);
			imgHiScoreG.fillRect(70,0,80,16);
			imgHiScoreG.setColor(Color.red);
			imgHiScoreG.drawString(Integer.toString(hiScore), 70,14);
			g.drawImage(imgHiScore,
					8+ leftOffset, 0+ topOffset, this);

			changeHiScore=0;
		}

		if (changeScore==1)
		{
			imgScoreG.setColor(Color.black);
			imgScoreG.fillRect(70,0,80,16);
			imgScoreG.setColor(Color.green);
			imgScoreG.drawString(Integer.toString(currentScore), 70,14);
			g.drawImage(imgScore,
					158+ leftOffset, 0+ topOffset, this);

			changeScore=0;
		}

		// update pac life info
		if (changePacRemain==1)
		{
			int i;
			for (i=1; i<pacRemain; i++)
			{
				g.drawImage(pac.imagePac[0][0],
						16*i+ leftOffset,
						canvasHeight-18+ topOffset, this);
			}
			g.drawImage(powerDot.imageBlank,
					16*i+ leftOffset,
					canvasHeight-17+ topOffset, this);

			changePacRemain=0;
		}
	}

	void move() {
		int k;
		int oldScore= currentScore;

        StatefulKnowledgeSession kSession = kBase.newStatefulKnowledgeSession();
        kSession.insert(pac);
		for (int i=0; i<4; i++){

            kSession.insert(ghostActors[i]);

        }
        kSession.fireAllRules();

		k=pac.move(pacmanKeyDir);

		if (k==1)	// eaten a dot
		{
			changeScore=1;
			currentScore += 10 * ((round+1)/2) ;
		}
		else if (k==2)	// eaten a powerDot
		{
			ghostScore =200;
		}

		if (maze.get().iTotalDotcount==0)
		{
			gameState= DEAD_WAIT;
			wait= WAIT_COUNT;
			newMaze=true;
			round++;
			return;
		}

		for (int i=0; i<4; i++)
		{
			k= ghostActors[i].testCollision(pac.myX, pac.myY);
			if (k==1)	// kill pac
			{
				pacRemain--;
				changePacRemain=1;
				gameState= DEAD_WAIT;	// stop the game
				wait= WAIT_COUNT;
				return;
			}
			else if (k==2)	// caught by pac
			{
				currentScore += ghostScore * ((round+1)/2) ;
				changeScore=1;
				ghostScore *=2;
			}
		}

		if (currentScore >hiScore)
		{
			hiScore= currentScore;
			changeHiScore=1;
		}

		if ( changeScore==1 )
		{
			if ( currentScore /10000 - oldScore/10000 > 0 )
			{
				pacRemain++;			// bonus
				changePacRemain=1;
			}
		}
	}

	public void update(Graphics g) {
		// System.out.println("update called");
		if (gameState == INIT_IMAGE)
			return;

		// seperate the timer from update
		if (signalMove!=0)
		{
			// System.out.println("update by timer");
			signalMove=0;

			if (wait!=0)
			{
				wait--;
				return;
			}

			switch (gameState)
			{
			case START_WAIT:
				if (pacmanKeyDir == DirectionMap.UP)	// the key to start game
					gameState=RUNNING;
				else
					return;
				break;
			case RUNNING:
				if (key==SUSPEND)
					gameState=SUSPENDED;
				else
					move();
				break;
			case DEAD_WAIT:
				if (pacRemain>0)
					startRound();
				else
					startGame();
				gameState= START_WAIT;
				wait= WAIT_COUNT;
				pacmanKeyDir = DirectionMap.DOWN;
				break;
			case SUSPENDED:
				if (key==SUSPEND)
					gameState=RUNNING;
				break;
			}
			key=NONE;
		}

		paintUpdate(g);
	}

	public void keyPressed(KeyEvent e) {
		switch (e.getKeyCode())
		{
		case KeyEvent.VK_RIGHT:
		case KeyEvent.VK_L:
			pacmanKeyDir = DirectionMap.RIGHT;
			break;
		case KeyEvent.VK_UP:
			pacmanKeyDir = DirectionMap.UP;
			break;
		case KeyEvent.VK_LEFT:
			pacmanKeyDir = DirectionMap.LEFT;
			break;
		case KeyEvent.VK_DOWN:
			pacmanKeyDir = DirectionMap.DOWN;
			break;
		case KeyEvent.VK_S:
			key=SUSPEND;
			break;
		case KeyEvent.VK_B:
			key=BOSS;
			break;
		}
	}

	public void windowClosing(WindowEvent e) {
		dispose();
	}

	public void run() {
		while (true)
		{
			try { Thread.sleep(timerPeriod); }
			catch (InterruptedException e)
			{
				return;
			}

			signalMove++;
			repaint();
		}
	}

	public void dispose() {
		//      timer.stop();	// deprecated
		// kill the thread
		timer.get().interrupt();
		// the off screen canvas
//		Image offScreen=null;
		offScreenG.get().dispose();
		offScreenG.set(null);

		// the objects
		maze.set(null);
		pac=null;
		powerDot=null;
		for (int i=0; i<4; i++)
			ghostActors[i]=null;
		ghostActors =null;

		// currentScore images
		imgScore=null;
		imgHiScore=null;
		imgScoreG.dispose();
		imgScoreG=null;
		imgHiScoreG.dispose();
		imgHiScoreG=null;

		super.dispose();

		finalized=true;
	}

	public boolean isFinalized() {
		return finalized;
	}

	public void setFinalized(boolean finalized) {
		this.finalized = finalized;
	}

// UNUSED ==============================================================================================================
	public void keyTyped(KeyEvent keyEvent) {}
	public void keyReleased(KeyEvent keyEvent) {}
	public void windowOpened(WindowEvent windowEvent) {}
	public void windowClosed(WindowEvent e) {}
	public void windowIconified(WindowEvent e) {}
	public void windowDeiconified(WindowEvent e) {}
	public void windowActivated(WindowEvent e) {}
	public void windowDeactivated(WindowEvent e) {}
}












