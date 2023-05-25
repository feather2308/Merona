package Tetris;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import java.awt.BorderLayout;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.ActionEvent;
import java.awt.CardLayout;
import java.awt.FlowLayout;

public class Launcher extends JFrame {

	private JPanel contentPane;
	private boolean isOpenedServer = false,
					isOpenedSingle = false,
					isOpenedMulti = false;

	private final ConnectServer connectServer = new ConnectServer();
	

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Launcher frame = new Launcher();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Launcher() {
		renderUI();
	}

	private void renderUI() {
		setTitle("Tetris Launcher");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 180, 150);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		CardLayout cardLayout = new CardLayout(0, 0);
		
		connectServer.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                multiPlay(connectServer.ip, connectServer.port);
            }
        });
		
		setContentPane(contentPane);
		contentPane.setLayout(cardLayout);
		
		JPanel firstPanel = new JPanel();
		contentPane.add(firstPanel, "name_982625890891300");
		JPanel playPanel = new JPanel();
		contentPane.add(playPanel, "name_982628514294600");
		
		JButton singleButton = new JButton("SinglePlay");
		singleButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(isOpenedSingle != true) singlePlay();
			}
		});
		
		JButton multiButton = new JButton("MultiPlay");
		multiButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(isOpenedMulti != true) {
					connectServer.setVisible(true);
				}
			}
		});
		
		playPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
		playPanel.add(singleButton);
		playPanel.add(multiButton);
		
		JButton backButton = new JButton("< Back");
		backButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				cardLayout.previous(contentPane);
			}
		});
		playPanel.add(backButton);
		
		JButton startButton = new JButton("Play");
		startButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				cardLayout.next(contentPane);
			}
		});
		firstPanel.setLayout(new BorderLayout(0, 15));
		firstPanel.add(startButton, BorderLayout.CENTER);
		
		JButton serverButton = new JButton("OpenServer");
		serverButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(isOpenedServer != true) server();
			}
		});
		firstPanel.add(serverButton, BorderLayout.NORTH);
		
		JButton exitButton = new JButton("Exit");
		exitButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		firstPanel.add(exitButton, BorderLayout.SOUTH);
	}
	
	void singlePlay() {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MyTetris frame = new MyTetris();
					frame.setVisible(true);
					frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
					isOpenedSingle = true;
					frame.addWindowListener(new WindowAdapter() {
					    public void windowClosing(WindowEvent e) {
					        isOpenedSingle = false;
					    }
					});
				} catch (Exception e) { }
			}
		});
	}
	
	void multiPlay(String IP, int port) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MyClient frameM = new MyClient(IP, port);
					frameM.setVisible(true);
					frameM.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
					isOpenedMulti = true;
					frameM.addWindowListener(new WindowAdapter() {
					    public void windowClosing(WindowEvent e) {
					        isOpenedMulti = false;
					    }
					});
				} catch (Exception e) { }
			}
		});
	}
	
	void server() {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MyServer server = new MyServer();
					server.setVisible(true);
					server.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
					isOpenedServer = true;
					server.addWindowListener(new WindowAdapter() {
					    public void windowClosing(WindowEvent e) {
					        isOpenedServer = false;
					    }
					});
				} catch (Exception e) { }
			}
		});
	}
}