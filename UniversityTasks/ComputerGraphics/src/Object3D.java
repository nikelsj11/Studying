import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;

class Cube3DShower extends JPanel implements Runnable{
    private Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    private BufferedImage context = new BufferedImage(screenSize.width, screenSize.height, BufferedImage.TYPE_INT_ARGB);
    private Color backColor = Color.DARK_GRAY;
    private static boolean perspective = true;
    private TQuad cube = new TQuad(screenSize.width, screenSize.height);

    //Конструктор
    public Cube3DShower() {
        Color back = backColor;
        this.setBackground(back);
        this.setLayout(null);

        JButton startButton = new JButton("ВКЛ/ВЫКЛ ПЕРСПЕКТИВУ");
        startButton.setBackground(Color.CYAN);
        startButton.setBounds(20, 20, 200, 40);
        this.add(startButton);

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                perspective = !perspective;
            }
        });

        // стороны куба
        double[][][] points = {
                // передняя сторона
                {{-250., 250., 250.}, {250., 250., 250.}, {250., -250., 250.}, {-250., -250., 250.}},
                // задняя сторона
                {{-250., 250., -250.}, {250., 250., -250.}, {250., -250., -250.}, {-250., -250., -250.}},
                // верхняя сторона
                {{-250., 250., 250.}, {250., 250., 250.}, {250., 250., -250.}, {-250., 250., -250.}},
                // нижняя сторона
                {{-250., -250., 250.}, {250., -250., 250.}, {250., -250., -250.}, {-250., -250., -250.}},
                // левая сторона
                {{-250., 250., 250.}, {-250., 250., -250.}, {-250., -250., -250.}, {-250., -250., 250.}},
                // правая сторона
                {{250., 250., 250.}, {250., 250., -250.}, {250., -250., -250.}, {250., -250., 250.}}
        };

        // нормали
        double[][] normals = {
                {0., 0., 1.},
                {0., 0., -1.},
                {0., 1., 0.},
                {0., -1., 0.},
                {-1., 0., 0.},
                {1., 0., 0.}
        };

        cube.setColor(Color.GREEN);     //цвет куба
        cube.setSides(points, normals); // инициализация сторон и нормалей куба
        new Thread(this).start(); // поток рисования
    }

    //переопределение метода отвечающего за рисования
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        // перерисовка куба в буффере
        repaintCube();
        // выводим буффер
        g.drawImage(context, 0, 0, screenSize.width, screenSize.height, this);
    }

    // перерисовка куба
    private void repaintCube(){
        Graphics2D g = context.createGraphics();

        // c перспективой или без
        if (perspective)
            cube.applyChanges();
        else
            cube.applyChangesWithoutPerspective();
        // заполняем фон
        g.setColor(backColor);
        g.fillRect(0, 0, screenSize.width, screenSize.width);

        // отрисовка поочередно каждой из сторон
        for(TSquare side: cube.sides){
            int[] x = {(int)side.points2D[0].x, (int)side.points2D[1].x, (int)side.points2D[2].x, (int)side.points2D[3].x};
            int[] y = {(int)side.points2D[0].y, (int)side.points2D[1].y, (int)side.points2D[2].y, (int)side.points2D[3].y};

            g.setColor(side.color);
            g.fillPolygon(x, y, 4);
        }

        // сохраняем результаты в буффер
        g.dispose();
    }


    // поток прорисовка
    @Override public void run() {
        while (true){ // бесконечно
            repaint();

            // вертим куб
            cube.rotateXY(0.005);
            cube.rotateXZ(-0.008);
            cube.rotateYZ(-0.0002);

            // пауза
                try { Thread.sleep(15); } catch (InterruptedException e) { e.printStackTrace();  }
        }
    }
}


class Object3D {
    // вывод окна
    public static void main(String[] args) { new PlayGround().run(new Cube3DShower(), "Дерево пифагора");}
}



