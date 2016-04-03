import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class PlayGround extends JApplet {
    public static void run(JPanel panel, String name) {
        final JFrame frame = new JFrame(name);
        final JApplet applet = new PlayGround();

        frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
        frame.setUndecorated(true);
        //frame.setAlwaysOnTop(true);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().setBackground(Color.white);
        frame.getContentPane().setLayout(null);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();

        JButton closeButton = new JButton("ЗАКРЫТЬ");
        closeButton.setBackground(Color.WHITE);
        closeButton.setBounds(0, 0, screenSize.width, 20);
        frame.getContentPane().add(closeButton);
        closeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                frame.dispose(); System.exit(0);
            }
        });

        applet.setBounds(0, 20, screenSize.width, screenSize.height-20);
        frame.getContentPane().add(applet);
        applet.getContentPane().add(panel);

        frame.setVisible(true);
    }

   // public static void main(String[] args) { run(new JPanel(), "Дерево пифагора"); }
}
