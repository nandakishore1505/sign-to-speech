import java.io.*;
import java.net.*;
import javax.swing.*;

public class GestureDisplay {

    public static void main(String[] args) {
        JFrame frame = new JFrame("Sign to Speech - Java Display");
        JLabel label = new JLabel("Waiting for gesture...", SwingConstants.CENTER);
        label.setFont(label.getFont().deriveFont(26f));
        frame.add(label);
        frame.setSize(500, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        try (ServerSocket serverSocket = new ServerSocket(5000)) {
            System.out.println("Java Display running... Waiting for gestures on port 5000");
            Socket socket = serverSocket.accept();
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String gesture;
            while ((gesture = in.readLine()) != null) {
                System.out.println("Received gesture: " + gesture);
                label.setText("Detected: " + gesture);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
