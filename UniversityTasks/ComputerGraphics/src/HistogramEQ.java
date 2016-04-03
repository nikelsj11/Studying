import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

class MakerHistogramEQ extends JPanel {
    Color backColor = Color.DARK_GRAY;
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    BufferedImage context = new BufferedImage(screenSize.width, screenSize.height, BufferedImage.TYPE_INT_ARGB);

    // конструктор
    public MakerHistogramEQ() {
        this.setBackground(backColor);
        this.setLayout(null);

        final JLabel fileTitle = new JLabel(""); fileTitle.setForeground(Color.white); fileTitle.setBounds(20, 10, 170, 40);
        this.add(fileTitle);

        JButton button = new JButton("ВЫБОР ФАЙЛА");
        button.setBackground(Color.CYAN);
        button.setBounds(20, 40, 170, 40);
        this.add(button);

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JFileChooser fileopen = new JFileChooser();
                int ret = fileopen.showDialog(null, "Открыть файл");
                if (ret == JFileChooser.APPROVE_OPTION) {
                    File file = fileopen.getSelectedFile();
                    fileTitle.setText(file.getName());
                    try { BufferedImage buf = ImageIO.read(file); start(buf); repaint();}
                    catch (IOException ee) {}
                }
            }
        });
    }


    // обрабатываем, выводим
    public void start(BufferedImage imageIn){
        Graphics2D g = context.createGraphics();

        BufferedImage orig = imageIn;
        BufferedImage copyOrig = histogramEqualization(orig);

        ArrayList<int[]> imgHistogram  = this.imageHistogram(imageIn);

        ArrayList<int[]> HQimgHistogram  = this.imageHistogram(copyOrig);

        int max = 0;

        int[] red = imgHistogram.get(0);
        int[] green = imgHistogram.get(1);
        int[] blue = imgHistogram.get(2);
        for(int item: green){ if (max<item) max = item; }
        for(int item: red){ if (max<item) max = item; }
        for(int item: blue){ if (max<item) max = item; }
        int[] red2 = HQimgHistogram.get(0);
        int[] green2 = HQimgHistogram.get(1);
        int[] blue2 = HQimgHistogram.get(2);
        for(int item: green2){ if (max<item) max = item; }
        for(int item: red2){ if (max<item) max = item; }
        for(int item: blue2){ if (max<item) max = item; }


        // фон
        g.setColor(this.backColor);
        g.fillRect(0, 0, screenSize.width, screenSize.height);

        // рисуем оригинальное изображение
        if (orig.getWidth()<screenSize.width/2)
            g.drawImage(orig, screenSize.width/4-orig.getWidth()/2, screenSize.height/2-orig.getHeight()/2, this);
        else
            g.drawImage(orig, 0, 0, screenSize.width/2, screenSize.height, this);

        // рисуем обработанное изображение
        if (copyOrig.getWidth()<screenSize.width/2)
            g.drawImage(copyOrig, screenSize.width/4-copyOrig.getWidth()/2+screenSize.width/2, screenSize.height/2-copyOrig.getHeight()/2, this);
        else
            g.drawImage(copyOrig, screenSize.width/2, 0, screenSize.width/2, screenSize.height, this);

        this.drawHistogram(g, imgHistogram, screenSize.width/4-(255*3)/2, screenSize.height-23, max);
        this.drawHistogram(g, HQimgHistogram, screenSize.width/4*3-(255*3)/2, screenSize.height-23, max);
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
        g.drawImage(context, 0, 0, this);
    }

    // получить гистограмму изображения
    public ArrayList<int[]> imageHistogram(BufferedImage input) {

        int[] rhistogram = new int[256];
        int[] ghistogram = new int[256];
        int[] bhistogram = new int[256];

        for(int i=0; i<rhistogram.length; i++) rhistogram[i] = 0;
        for(int i=0; i<ghistogram.length; i++) ghistogram[i] = 0;
        for(int i=0; i<bhistogram.length; i++) bhistogram[i] = 0;

        for(int i=0; i<input.getWidth(); i++) {
            for(int j=0; j<input.getHeight(); j++) {

                int red = new Color(input.getRGB (i, j)).getRed();
                int green = new Color(input.getRGB (i, j)).getGreen();
                int blue = new Color(input.getRGB (i, j)).getBlue();

                rhistogram[red]++;
                ghistogram[green]++;
                bhistogram[blue]++;

            }
        }

        ArrayList<int[]> hist = new ArrayList<int[]>();

        hist.add(rhistogram);
        hist.add(ghistogram);
        hist.add(bhistogram);

        return hist;

    }


    public void drawHistogram(Graphics2D g,ArrayList<int[]> histogram, int x0, int y0, int factor){
        int[] red = histogram.get(0);
        int[] green = histogram.get(1);
        int[] blue = histogram.get(2);

        double max = (200./factor);

        g.setColor(Color.RED);

        for(int i=0; i<red.length; i++){
            g.drawLine(x0+i, y0, x0+i, y0-(int)(red[i]*max));
        }
        g.setColor(Color.green);

        for(int i=0; i<green.length; i++){
            g.drawLine(x0+i+red.length, y0, x0+i+red.length, y0-(int)(green[i]*max));
        }
        g.setColor(Color.BLUE);

        for(int i=0; i<blue.length; i++){
            g.drawLine(x0+i+red.length+green.length, y0, x0+i+red.length+green.length, y0-(int)(blue[i]*max));
        }


    }


    private BufferedImage histogramEqualization(BufferedImage original) {

        int red, green, blue, alpha;
        int newPixel;

        ArrayList<int[]> histLUT = histogramEqualizationLookUpTable(original);

        BufferedImage histogramEQ = new BufferedImage(original.getWidth(), original.getHeight(), original.getType());

        for(int i=0; i<original.getWidth(); i++) {
            for(int j=0; j<original.getHeight(); j++) {

                alpha = new Color(original.getRGB (i, j)).getAlpha();
                red = new Color(original.getRGB (i, j)).getRed();
                green = new Color(original.getRGB (i, j)).getGreen();
                blue = new Color(original.getRGB (i, j)).getBlue();

                red = histLUT.get(0)[red];
                green = histLUT.get(1)[green];
                blue = histLUT.get(2)[blue];

                newPixel = colorToRGB(alpha, red, green, blue);

                histogramEQ.setRGB(i, j, newPixel);

            }
        }

        return histogramEQ;

    }

    // Get the histogram equalization lookup table for separate R, G, B channels
    private ArrayList<int[]> histogramEqualizationLookUpTable(BufferedImage input) {

        ArrayList<int[]> imageHist = imageHistogram(input);

        ArrayList<int[]> imageLUT = new ArrayList<int[]>();

        int[] rhistogram = new int[256];
        int[] ghistogram = new int[256];
        int[] bhistogram = new int[256];

        for(int i=0; i<rhistogram.length; i++) rhistogram[i] = 0;
        for(int i=0; i<ghistogram.length; i++) ghistogram[i] = 0;
        for(int i=0; i<bhistogram.length; i++) bhistogram[i] = 0;

        long sumr = 0;
        long sumg = 0;
        long sumb = 0;

        float scale_factor = (float) (255.0 / (input.getWidth() * input.getHeight()));

        for(int i=0; i<rhistogram.length; i++) {
            sumr += imageHist.get(0)[i];
            int valr = (int) (sumr * scale_factor);
            if(valr > 255) {
                rhistogram[i] = 255;
            }
            else rhistogram[i] = valr;

            sumg += imageHist.get(1)[i];
            int valg = (int) (sumg * scale_factor);
            if(valg > 255) {
                ghistogram[i] = 255;
            }
            else ghistogram[i] = valg;

            sumb += imageHist.get(2)[i];
            int valb = (int) (sumb * scale_factor);
            if(valb > 255) {
                bhistogram[i] = 255;
            }
            else bhistogram[i] = valb;
        }

        imageLUT.add(rhistogram);
        imageLUT.add(ghistogram);
        imageLUT.add(bhistogram);

        return imageLUT;

    }

    // Convert R, G, B, Alpha to standard 8 bit
    private static int colorToRGB(int alpha, int red, int green, int blue) {

        int newPixel = 0;
        newPixel += alpha; newPixel = newPixel << 8;
        newPixel += red; newPixel = newPixel << 8;
        newPixel += green; newPixel = newPixel << 8;
        newPixel += blue;

        return newPixel;

    }
}


public class HistogramEQ {
    public static void main(String[] args) { new PlayGround().run(new MakerHistogramEQ(), "Выравнивание гистограммы");}
}
