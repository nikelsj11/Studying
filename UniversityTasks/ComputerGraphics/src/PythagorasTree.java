import javax.swing.*;
import java.awt.*;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import static java.lang.Math.cos;
import static java.lang.Math.sin;
import static java.lang.Math.PI;


class PaintPythagorasTree extends JPanel implements Runnable {
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
    public PaintPythagorasTree() {
        Color back = backColor;
        this.setBackground(back);
        this.setLayout(null);

        JButton startButton = new JButton("НАРИСОВАТЬ");
        startButton.setBackground(Color.CYAN);
        startButton.setBounds(20, 20, 150, 40);
        this.add(startButton);

        JLabel degL = new JLabel("Угол"); degL.setForeground(Color.white); degL.setBounds(20, 60, 150, 40);
        this.add(degL);

        final JTextField deg = new JTextField("45");
        deg.setBackground(Color.lightGray);
        deg.setBounds(20, 90, 150, 30);
        this.add(deg);

        JLabel sizeL = new JLabel("Нач. размер"); sizeL.setForeground(Color.white); sizeL.setBounds(20, 130, 150, 40);
        this.add(sizeL);

        final JTextField size = new JTextField("259");
        size.setBackground(Color.lightGray);
        size.setBounds(20, 160, 150, 30);
        this.add(size);

        JLabel depL = new JLabel("Глубина"); depL.setForeground(Color.white); depL.setBounds(20, 200, 150, 40);
        this.add(depL);

        final JTextField dep = new JTextField("17");
        dep.setBackground(Color.lightGray);
        dep.setBounds(20, 230, 150, 30);
        this.add(dep);

        JRadioButton fill = new JRadioButton("ЗАКРАСИТЬ");
        fill.setForeground(Color.WHITE);
        fill.setBackground(backColor);
        fill.setActionCommand("fill");
        fill.setBounds(20, 270, 150, 30);
        this.add(fill);

        JRadioButton line = new JRadioButton("ЛИНИЯМИ");
        line.setForeground(Color.WHITE);
        line.setBackground(backColor);
        line.setActionCommand("line");
        line.setBounds(20, 290, 150, 30);
        this.add(line);

        JRadioButton bro = new JRadioButton("БРЕЗЕНХЭМОМ");
        bro.setForeground(Color.WHITE);
        bro.setBackground(backColor);
        bro.setActionCommand("bro");
        bro.setBounds(20, 310, 150, 30);
        this.add(bro);

        final ButtonGroup groupType = new ButtonGroup();
        groupType.add(fill);
        groupType.add(line);
        groupType.add(bro);

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                start(Integer.parseInt(size.getText()), Integer.parseInt(dep.getText()),
                        Double.parseDouble(deg.getText()) * PI / 180, groupType.getSelection().getActionCommand());
            }
        });
    }

    //фун-я начала рисования
    public void start(int sWidth, int sDepth, double sDeg, String sFill){
        this.sWidth = sWidth;
        this.sDeg = sDeg;
        this.sDepth = sDepth;
        this.sFill = sFill;

        rewrite = true;

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
    private final void paintFractal(int depth, int x0, int y0, double a, double fi, double alpha, boolean is_start){
         int x1 = x0 + (int)( a * cos(fi));
         int y1 = y0 - (int)( a * sin(fi));
         int x2 = x0 - (int)( a * sin(fi));
         int y2 = y0 - (int)( a * cos(fi));
         int x3 = x2 + (int)( a * cos(fi));
         int y3 = y2 - (int)( a * sin(fi));
         int x4 = x2 + (int)( a * cos(alpha) * cos(fi+alpha));
         int y4 = y2 - (int)( a * cos(alpha) * sin(fi+alpha));

         if (sFill == "fill")
            _byPoligons(depth, x0, y0, x1, y1, x2, y2, x3, y3, x4, y4);
         else if (sFill == "line")
             _byLines( x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, is_start);
         else if (sFill == "bro")
             _byLinesWithBresenham(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, is_start);

         if ((depth>= sDepth) | (rewrite)) return;
         paintFractal(depth+1, x2, y2, a*cos(alpha), fi+alpha, alpha, false);
         paintFractal(depth+1, x4, y4, a*sin(alpha), alpha+fi - PI/2, alpha, false);
    }
    
    //Прорисовка линиями
    private final void _byLines(int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4, boolean is_start){
        Graphics2D g = context.createGraphics(); g.setColor(Color.WHITE);  g.setStroke(pen);
        if (is_start) g.drawLine(x0, y0, x1, y1);
            g.drawLine(x0, y0, x2, y2);
            g.drawLine(x2, y2, x3, y3);
            g.drawLine(x1, y1, x3, y3);
            g.drawLine(x2, y2, x3, y3);
            g.drawLine(x3, y3, x4, y4);
            g.drawLine(x2, y2, x4, y4);
        g.dispose();
        repaint();
    }

    //Прорисовка Закрашенными полигонами
    private final void _byPoligons(int depth, int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4) {
        Graphics2D g = context.createGraphics();

        GradientPaint primary = new GradientPaint(
                x1, y1, new Color(233-((233-11)/sDepth*depth), 123+((160-122)/sDepth*depth), 0, 210),
                x0, y0, new Color(175-((175-11)/sDepth*depth), 93+((125-91)/sDepth*depth), 0, 200), true);

        int[] xPoints = {x0, x1, x3, x4, x2};
        int[] yPoints = {y0, y1, y3, y4, y2};

        g.setPaint(primary);
        g.fillPolygon(xPoints, yPoints, 5);

        g.dispose();
        repaint();
    }

    //Прорисовка линиями с алгоритмом Брезенхэма
    private final void _byLinesWithBresenham(int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4, boolean is_start){
        Graphics2D g = context.createGraphics();
            g.setColor(Color.WHITE);
            g.setStroke(pen);
        if (is_start) _bresenhamLineAlgorithm(x0, y0, x1, y1, g);
        _bresenhamLineAlgorithm(x0, y0, x2, y2, g);
        _bresenhamLineAlgorithm(x2, y2, x3, y3, g);
        _bresenhamLineAlgorithm(x1, y1, x3, y3, g);
        _bresenhamLineAlgorithm(x2, y2, x3, y3, g);
        _bresenhamLineAlgorithm(x3, y3, x4, y4, g);
        _bresenhamLineAlgorithm(x2, y2, x4, y4, g);
        g.dispose();
        repaint();
    }

    //Алгоритм Брезенхэма целочисленный
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

    //поток рисования
    public void run() {
        long strartTime = System.currentTimeMillis();
        rewrite = false;
        paintFractal(0, screenSize.width / 2 - sWidth / 2, screenSize.height - 50, sWidth, 0, sDeg, true);

        Graphics g = context.getGraphics();
                 g.setColor(Color.red);
                 g.drawString(""+(System.currentTimeMillis()-strartTime)+" ms", 20, screenSize.height-50);
                 g.dispose();
        repaint();
    }
}



public class PythagorasTree extends JApplet {
    public static void main(String[] args) { new PlayGround().run(new PaintPythagorasTree(), "Дерево пифагора");}
}
