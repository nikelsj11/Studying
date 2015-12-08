import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.util.Random;

import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;

class PaintBresenhamAlgorithms extends JPanel implements Runnable{
    private Thread thread;
    private Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    private BufferedImage context = new BufferedImage(screenSize.width, screenSize.height, BufferedImage.TYPE_INT_ARGB);
    private Color backColor = Color.BLACK;
    private BasicStroke pen = new BasicStroke(1);
    int sWidth = 100, sDepth = 20;
    double sDeg = PI/2;
    String sFill;
    private boolean rewrite;

    //Конструктор
    public PaintBresenhamAlgorithms() {
        Color back = backColor;
        this.setBackground(back);
        this.setLayout(null);

        JButton startButton = new JButton("НАРИСОВАТЬ");
        startButton.setBackground(Color.CYAN);
        startButton.setBounds(20, 20, 150, 40);
        this.add(startButton);

        JRadioButton circle = new JRadioButton("OКРУЖНОСТИ");
        circle.setForeground(Color.WHITE);
        circle.setBackground(backColor);
        circle.setSelected(true);
        circle.setActionCommand("circle");
        circle.setBounds(20, 70, 150, 30);
        this.add(circle);

        JRadioButton line = new JRadioButton("ЛИНИИ");
        line.setForeground(Color.WHITE);
        line.setBackground(backColor);
        line.setActionCommand("line");
        line.setBounds(20, 90, 150, 30);
        this.add(line);

        JRadioButton ellipse = new JRadioButton("ОВАЛЫ");
        ellipse.setForeground(Color.WHITE);
        ellipse.setBackground(backColor);
        ellipse.setActionCommand("ellipse");
        ellipse.setBounds(20, 110, 150, 30);
        this.add(ellipse);

        final ButtonGroup groupType = new ButtonGroup();
        groupType.add(circle);
        groupType.add(line);
        groupType.add(ellipse);

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                start(groupType.getSelection().getActionCommand());
            }
        });
    }

    //фун-я начала рисования
    public void start(String sFill){
        this.sFill = sFill;

        rewrite = true;

        context = new BufferedImage(screenSize.width, screenSize.height, BufferedImage.TYPE_INT_ARGB);
        Graphics g = context.getGraphics();
        g.setColor(backColor);
        g.fillRect(0, 0, screenSize.width, screenSize.height);
        g.dispose();

        repaint(100);

        thread = new Thread(this);
        thread.start();
    }

    //переопределение метода отвечающего за рисования
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (rewrite){
            g.setColor(backColor);
            g.fillRect(0, 0, screenSize.width, screenSize.height);
        }
        g.setColor(Color.BLACK);
        g.drawImage(context, 0, 0, screenSize.width, screenSize.height, this);
    }

    //Рисование фрактала
    private final void paintObjects(){

        if (sFill == "circle")
            _PaintCircles();
        else if (sFill == "line")
            _PaintLines();
        else if (sFill == "ellipse")
            _PaintEllipse();

    }

    //Рисование линиями с алгоритмом Брезенхэма
    private final void _PaintLines(){
        Graphics2D g = context.createGraphics();
        g.setColor(Color.WHITE);
        g.setStroke(pen);

        int x0 = screenSize.width/2;
        int y0 = screenSize.height/2;

        int x2, y2;

        for(int i=0; i<=360; i++){
            double deg =  (PI/180*i);
            x2 = x0 + (int)(500 * cos(deg));
            y2 = y0 - (int)(500 * sin(deg));
            Random rand = new Random();
            g.setColor(new Color(rand.nextFloat(), rand.nextFloat(), rand.nextFloat()));
            _bresenhamLineAlgorithm(x2, y2, x0, y0, g);
        }
        g.dispose();
    repaint();
    }

    //Рисование окружностями с алгоритмом Брезенхэма
    private final void _PaintCircles(){
        Graphics2D g = context.createGraphics();
        g.setColor(Color.WHITE);
        g.setStroke(pen);

        int x0 = screenSize.width/2;
        int y0 = screenSize.height/2;


        for(int i=1; i<=500; i += 5){
            Random rand = new Random();
            g.setColor(new Color(rand.nextFloat(), rand.nextFloat(), rand.nextFloat()));
            _bresenhamCircleAlgorithm(x0, y0, i, g);
        }

        g.dispose();
        repaint();
    }

    //Рисование элипсами с алгоритмом Брезенхэма
    private final void _PaintEllipse(){
        Graphics2D g = context.createGraphics();
        g.setColor(Color.WHITE);
        g.setStroke(pen);

        int x0 = screenSize.width/2;
        int y0 = screenSize.height/2;


        for(int i=1; i<=500; i += 9){
            Random rand = new Random();
            g.setColor(new Color(rand.nextFloat(), rand.nextFloat(), rand.nextFloat()));
            _bresenhamEllipseAlgorithm(x0, y0, i, i - (i/3), g);
        }
        g.dispose();
        repaint();
    }

    //Алгоритм Брезенхэма рисования линий (целочисленный)
    private void _bresenhamLineAlgorithm(int x1, int y1, int x2, int y2, Graphics g) {
        int dx = Math.abs(x2-x1), dy = Math.abs(y2-y1);
        int sx = (x2-x1)>0?1:((x2-x1)==0?0:-1);
        int sy = (y2-y1)>0?1:((y2-y1)==0?0:-1);
        int tx, ty;

        if (dx>=dy){
            tx = sx; ty = 0;
        } else {
            int z=dx; dx=dy; dy=z;
            tx=0; ty=sy;
        }

        int scount = 2*dy;
        int count = scount-dx;
        int dcount = count-dx;

        while(true){
            dx-=1;
            if (dx<-1) break;
            g.drawLine(x1, y1, x1, y1);
            if (count>=0) {
                x1+=sx; y1+=sy;
                count += dcount;
            } else {
                x1+=tx; y1+=ty;
                count += scount;
            }
        }
    }

    //Алгоритм Брезенхэма рисования окружностей
    private void _bresenhamCircleAlgorithm(int x, int y, int r, Graphics g) {
        int sx=0;
        int sy=r;
        int d=3-2*r;
        while(sx<=sy) {
            g.drawLine(x+sx, y-sy, x+sx, y-sy);
            g.drawLine(x+sx, y+sy, x+sx, y+sy);
            g.drawLine(x-sx, y-sy, x-sx, y-sy);
            g.drawLine(x-sx, y+sy, x-sx, y+sy);

            g.drawLine(x+sy, y+sx, x+sy, y+sx);
            g.drawLine(x-sy, y+sx, x-sy, y+sx);
            g.drawLine(x+sy, y-sx, x+sy, y-sx);
            g.drawLine(x-sy, y-sx, x-sy, y-sx);

            if (d<0) {
                d = d + 4 * sx + 6;
            } else {
                d = d + 4 * (sx - sy) + 10;
                sy = sy - 1;
            }
            sx += 1;
        }
    }

    //Алгоритм Брезенхэма рисования элипса
    private void _bresenhamEllipseAlgorithm (int x0, int y0, int width, int height, Graphics g) {
        int a2 = width * width;
        int b2 = height * height;
        int fa2 = 4 * a2, fb2 = 4 * b2;
        int  x, y, sigma;

    /* first half */
        for (x = 0, y = height, sigma = 2*b2+a2*(1-2*height); b2*x <= a2*y; x++)
        {
            g.drawLine(x0 + x, y0 + y, x0 + x, y0 + y);
            g.drawLine(x0 - x, y0 + y, x0 - x, y0 + y);
            g.drawLine(x0 + x, y0 - y, x0 + x, y0 - y);
            g.drawLine(x0 - x, y0 - y, x0 - x, y0 - y);
            if (sigma >= 0)
            {
                sigma += fa2 * (1 - y);
                y--;
            }
            sigma += b2 * ((4 * x) + 6);
        }

    /* second half */
        for (x = width, y = 0, sigma = 2*a2+b2*(1-2*width); a2*y <= b2*x; y++)
        {
            g.drawLine(x0 + x, y0 + y, x0 + x, y0 + y);
            g.drawLine(x0 - x, y0 + y, x0 - x, y0 + y);
            g.drawLine(x0 + x, y0 - y, x0 + x, y0 - y);
            g.drawLine(x0 - x, y0 - y, x0 - x, y0 - y);
            if (sigma >= 0)
            {
                sigma += fb2 * (1 - x);
                x--;
            }
            sigma += a2 * ((4 * y) + 6);
        }
    }
    
    //Поток рисования
    public void run() {
        long strartTime = System.currentTimeMillis();
        rewrite = false;
        paintObjects();

        Graphics g = context.getGraphics();
        g.setColor(Color.red);
        g.drawString(""+(System.currentTimeMillis()-strartTime)+" ms", 20, screenSize.height-50);
        g.dispose();
        repaint();
    }

}



public class BresenhamAlgorithms {
    public static void main(String[] args) { new PlayGround().run(new PaintBresenhamAlgorithms(), "Алгоритмы Брезенхема");}
}
