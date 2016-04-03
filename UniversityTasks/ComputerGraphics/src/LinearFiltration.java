import com.sun.javafx.tk.quantum.PixelUtils;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import static java.lang.StrictMath.abs;


class MakerFiltration extends JPanel{
    Color backColor = Color.DARK_GRAY;
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    BufferedImage orig;
    BufferedImage copyOrig;

    // конструктор
    public MakerFiltration() {
        Color back = backColor;
        this.setBackground(back);
        this.setLayout(null);

        JButton startButton = new JButton("ФИЛЬТРОВАТЬ");
        startButton.setBackground(Color.CYAN);
        startButton.setBounds(20, 20, 170, 40);
        this.add(startButton);

        final JLabel degL = new JLabel(""); degL.setForeground(Color.white); degL.setBounds(20, 60, 170, 40);
        this.add(degL);


        final JTextArea matr = new JTextArea();
        matr.setBounds(20, 160, 200, 200);
        this.add(matr);

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                start(matr.getText());
            }
        });


        JButton button = new JButton("ВЫБОР ФАЙЛА");
        button.setBackground(Color.CYAN);
        button.setBounds(20, 100, 170, 40);
        this.add(button);

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JFileChooser fileopen = new JFileChooser();
                int ret = fileopen.showDialog(null, "Открыть файл");
                if (ret == JFileChooser.APPROVE_OPTION) {
                    File file = fileopen.getSelectedFile();
                    degL.setText(file.getName());
                    try { orig = ImageIO.read(file);  repaint();}
                    catch (IOException ee) {}
                }
            }
        });
    }

    // производим линейную фильтрацию и выводим
    public  void start(String mart){
        String[] str = mart.split("\n");

        int count = Integer.parseInt(str[0]);
        int[][] filter = new int[count][count];

        int j = -1;
        for (String crtLine : str) {
            int i = 0;
            if (j == -1) { j++; continue;}
            String[] items = crtLine.split(" ");
            for (String crtItem: items) {
                filter[j][i++] = Integer.parseInt(crtItem);
            }
            j++;
        }


           run(filter);
           repaint();
    }


    public void run(int[][] filter) {
        copyOrig = createBufferedImage(orig);

        int M = copyOrig.getWidth();
        int N = copyOrig.getHeight();

        double s = 0;
        for (int[] i: filter)
            for(int j: i)
                s+=(j);

        s = 1/s;
        int K = filter[0].length/2;
        int L = filter.length/2;


        for (int v = L; v <= N - L - 1; v++) {
            for (int u = K; u <= M - K - 1; u++) {
                double sum_r = 0;
                double sum_g = 0;
                double sum_b = 0;
                for (int j = -L; j <= L; j++) {
                    for (int i = -K; i <= K; i++) {
                        Color col = new Color(orig.getRGB(u + i, v + j));
                        int p_r = col.getRed();
                        int p_g = col.getGreen();
                        int p_b = col.getBlue();
                        double factor = filter[j + L][i + K];
                        sum_r = sum_r + factor * (p_r);
                        sum_g = sum_g + factor * (p_g);
                        sum_b = sum_b + factor * (p_b);
                    }
                }
                int q_r = (int) (s * sum_r);
                int q_g = (int) (s * sum_g);
                int q_b = (int) (s * sum_b);

                if (q_r < 0)   q_r = 0;
                if (q_r > 255) q_r = 255;
                if (q_g < 0)   q_g = 0;
                if (q_g > 255) q_g = 255;
                if (q_b < 0)   q_b = 0;
                if (q_b > 255) q_b = 255;
                copyOrig.setRGB(u, v, new Color(q_r, q_g, q_b).getRGB());
            }
        }


    }



    // копия изображения
    public BufferedImage createBufferedImage(BufferedImage image){
            BufferedImage b = new BufferedImage(image.getWidth(), image.getHeight(), image.getType());
            Graphics g = b.getGraphics();
            g.drawImage(image, 0, 0, null);
            g.dispose();
            return b;
    }

    //переопределение метода отвечающего за рисования
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (orig!=null)
            if (orig.getWidth()<screenSize.width/2)
                g.drawImage(orig, screenSize.width/4-orig.getWidth()/2, screenSize.height/2-orig.getHeight()/2, this);
            else
                g.drawImage(orig, screenSize.width/2, 0, screenSize.width/2, screenSize.height, this);
        if (copyOrig!=null)
            if (copyOrig.getWidth()<screenSize.width/2)
                g.drawImage(copyOrig, screenSize.width/4-copyOrig.getWidth()/2+screenSize.width/2, screenSize.height/2-copyOrig.getHeight()/2, this);
            else
                g.drawImage(copyOrig, screenSize.width/2, 0, screenSize.width/2, screenSize.height, this);
    }


}


public class LinearFiltration {
    public static void main(String[] args) { new PlayGround().run(new MakerFiltration(), "Линейная фильтрация");}
}
