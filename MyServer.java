package Tetris;

import java.awt.EventQueue;
import java.io.*;
import java.net.*;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import java.awt.BorderLayout;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JButton;
import java.awt.GridLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.List;
import java.util.ArrayList;

public class MyServer extends JFrame {

    private Socket socket = null;
    private ServerSocket serverSocket = null;
    private int port = 30000;
    private boolean isOpened = false;
    private int maxClients = 2;
    private int connectedClients = 0;
    private List<ClientHandler> clientHandlers = new ArrayList<>();

    private JPanel contentPane;
    private JTextField textIPField;
    private JTextField textPortField;
    private JLabel lblStatusLabel;

    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            public void run() {
                try {
                    MyServer frame = new MyServer();
                    frame.setVisible(true);
                } catch (Exception e) {    }
            }
        });
    }

    public MyServer() {
        setTitle("TetrisServer");
        try {
            renderUI();
        } catch (UnknownHostException e) { }
    }

    public void initServer() throws IOException {
        String portText = textPortField.getText();
        try {
            port = Integer.parseInt(portText);
            serverSocket = new ServerSocket(port);
            acceptClientConnection();
            isOpened = true;
            lblStatusLabel.setText("Status: Open");
        } catch (NumberFormatException e) {
            System.out.println("Invalid port number: " + portText);
        }
    }

    public void closeServer() throws IOException {
        if(serverSocket != null) {
            isOpened = false;
            serverSocket.close();
            for (ClientHandler clientHandler : clientHandlers) {
                clientHandler.closeSocket();
            }
            lblStatusLabel.setText("Status: Close");
        }
    }

    private void acceptClientConnection() {
        Thread thread = new Thread() {
            public void run() {
                try {
                    while (isOpened) {
                        socket = serverSocket.accept();
                        System.out.println("Client connected: " + socket.getInetAddress());

                        if (connectedClients < maxClients) {
                            ClientHandler clientHandler = new ClientHandler(socket, clientHandlers);
                            clientHandlers.add(clientHandler);
                            clientHandler.start();

                            connectedClients++;
                        } else {
                            socket.close();
                            System.out.println("Connection refused. Maximum clients reached.");
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };
        thread.start();
    }


    private class ClientHandler extends Thread {
        private Socket clientSocket;
        private ObjectInputStream in;
        private ObjectOutputStream out;
        private String clientId;
        private boolean calling = true;

        public ClientHandler(Socket clientSocket, List<ClientHandler> clientHandlers) throws IOException {
            this.clientSocket = clientSocket;
            this.in = new ObjectInputStream(clientSocket.getInputStream());
            this.out = new ObjectOutputStream(clientSocket.getOutputStream());
        }

        @Override
        public void run() {
            try {
                while (calling) {
                    Object receivedObject = in.readObject();
                    if (receivedObject instanceof TetrisData) {
                        TetrisData receivedData = (TetrisData) receivedObject;
                        System.out.println("클라이언트로부터 받은 객체: " + receivedData);

                        // 다른 클라이언트들에게 객체 전송
                        for (ClientHandler clientHandler : clientHandlers) {
                            if (clientHandler != this) {
                                clientHandler.sendObject(receivedData);
                            }
                        }
                    }
                }

                // 클라이언트와의 연결 종료
                in.close();
                out.close();
            } catch (IOException | ClassNotFoundException e) {
                e.printStackTrace();
            } finally {
                // 클라이언트 소켓 닫기
                closeSocket();
            }
        }

        public void sendObject(TetrisData data) {
            try {
                out.writeObject(data);
                out.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void closeSocket() {
            if (clientSocket != null && !clientSocket.isClosed()) {
                try {
                    clientSocket.close();
                } catch (IOException e) { }
            }
        }
    }

    public void renderUI() throws UnknownHostException {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(100, 100, 450, 300);
        contentPane = new JPanel();
        contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

        setContentPane(contentPane);
        contentPane.setLayout(new BorderLayout(0, 0));

        JPanel panel = new JPanel();
        contentPane.add(panel, BorderLayout.CENTER);

        JLabel lblIPLabel = new JLabel("IP");

        textIPField = new JTextField();
        textIPField.setEditable(false);
        textIPField.setColumns(10);

        JLabel lblPortLabel = new JLabel("Port");

        textPortField = new JTextField();
        textPortField.setText("30000");
        textPortField.setColumns(10);
        panel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
        panel.add(lblIPLabel);
        panel.add(textIPField);
        panel.add(lblPortLabel);
        panel.add(textPortField);

        lblStatusLabel = new JLabel("Status: Close");
        contentPane.add(lblStatusLabel, BorderLayout.SOUTH);

        JPanel panel_1 = new JPanel();
        contentPane.add(panel_1, BorderLayout.EAST);
        panel_1.setLayout(new GridLayout(0, 1, 0, 0));

        JButton btnOpenButton = new JButton("Open");
        btnOpenButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if(isOpened != true) {
                    try {
                        initServer();
                    } catch (IOException e1) { };
                }
            }
        });
        panel_1.add(btnOpenButton);

        JButton btnCloseButton = new JButton("Close");
        btnCloseButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if(isOpened) {
                    try {
                        closeServer();
                    } catch (IOException e1) { }
                }
            }
        });
        panel_1.add(btnCloseButton);

        textIPField.setText(InetAddress.getLocalHost().getHostAddress());
    }
}
