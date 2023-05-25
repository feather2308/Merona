package Tetris;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import java.awt.BorderLayout;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

import java.io.*;
import java.net.*;

public class MyTetris extends JFrame {

	private JPanel contentPane;
	private static TetrisCanvas tetrisCanvas;
	private MultiTetrisCanvas multiTetrisCanvas;
	private static JLabel lblScoreLabel;
	private static JLabel lblLineLabel;
	private static JMenuItem mntmStartMenuItem;
	private JMenuItem mntmNewMenuItem;
	private JLabel lblNewLabel;
	private JLabel lblNewLabel_1;
	private JMenuItem mntmNewMenuItem_1;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MyTetris frame = new MyTetris();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public MyTetris() {
		renderUI();
	}

	public static TetrisCanvas getTetrisCanvas() {
		return tetrisCanvas;
	}
	public static JLabel getLblScoreLabel() {
		return lblScoreLabel;
	}
	public static JLabel getLblLineLabel() {
		return lblLineLabel;
	}
	public static JMenuItem getMntmNewMenuItem() {
		return mntmStartMenuItem;
	}
	
	private void renderUI() {
		setResizable(false);
		setTitle("테트리스");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 400, 600);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		JMenu mnGameMenu = new JMenu("게임");
		menuBar.add(mnGameMenu);
		
		mntmStartMenuItem = new JMenuItem("시작");
		mntmStartMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				tetrisCanvas.start();
				mntmStartMenuItem.setEnabled(false);
			}
		});
		mnGameMenu.add(mntmStartMenuItem);
		
		JMenuItem mntmExitMenuItem = new JMenuItem("종료");
		mntmExitMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		mnGameMenu.add(mntmExitMenuItem);
		
		JMenu mnNewMenu_1 = new JMenu("Extra");
		menuBar.add(mnNewMenu_1);
		
		JMenuItem mntmNewMenuItem_2 = new JMenuItem("확장");
		mntmNewMenuItem_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				renderUIMulti();
			}
		});
		mnNewMenu_1.add(mntmNewMenuItem_2);
		
		mntmNewMenuItem = new JMenuItem("Server");
		mntmNewMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					serverHandler sh = new serverHandler(3000);
					sh.start();
				} catch (Exception e1) { }
			}
		});
		mnNewMenu_1.add(mntmNewMenuItem);
		
		mntmNewMenuItem_1 = new JMenuItem("Client");
		mntmNewMenuItem_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					clientHandler ch = new clientHandler("localhost", 3000);
					ch.start();
				} catch (Exception e1) { }
			}
		});
		mnNewMenu_1.add(mntmNewMenuItem_1);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(new BorderLayout(0, 0));
		
		tetrisCanvas = new TetrisCanvas();
		contentPane.add(tetrisCanvas, BorderLayout.CENTER);
		tetrisCanvas.setLayout(null);
		
		lblNewLabel = new JLabel("-NEXT-");
		lblNewLabel.setBounds(300, 15, 45, 15);
		lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		tetrisCanvas.add(lblNewLabel);
		
		lblNewLabel_1 = new JLabel("-SAVE-");
		lblNewLabel_1.setBounds(300, 140, 44, 15);
		lblNewLabel_1.setHorizontalAlignment(SwingConstants.CENTER);
		tetrisCanvas.add(lblNewLabel_1);
		
		lblScoreLabel = new JLabel("Score");
		lblScoreLabel.setBounds(270, 475, 95, 15);
		lblScoreLabel.setHorizontalAlignment(SwingConstants.LEFT);
		tetrisCanvas.add(lblScoreLabel);
		
		lblLineLabel = new JLabel("Line");
		lblLineLabel.setBounds(270, 495, 60, 15);
		lblLineLabel.setHorizontalAlignment(SwingConstants.LEFT);
		tetrisCanvas.add(lblLineLabel);
	}
	
	private void renderUIMulti() {
		setBounds(100, 100, 700, 600);
		multiTetrisCanvas = new MultiTetrisCanvas(new TetrisData());
		contentPane.add(multiTetrisCanvas, BorderLayout.EAST);
		multiTetrisCanvas.setLayout(null);
	}
	
	private class serverHandler extends Thread {
		private ServerSocket socket;
		private Socket client;
		private BufferedReader in;
		private PrintWriter out;
		private ObjectInputStream inObj;
		private ObjectOutputStream outObj;
		
		public serverHandler(int port){
			try {
				socket = new ServerSocket(port);
			} catch (IOException e) { }
		}
		
		public void run() {
			while(true) {
				System.out.println("헉runserver");
				try {
					client = socket.accept();
					in = new BufferedReader(new InputStreamReader(client.getInputStream()));
					out = new PrintWriter(new OutputStreamWriter(client.getOutputStream()));
					inObj = new ObjectInputStream(client.getInputStream());
					outObj = new ObjectOutputStream(client.getOutputStream());
					while(true) {
						if(in.read()==1) {
							out.write(1);
							out.flush();
							break;
						}
					}
					while(true) {
						Object receivedObject = inObj.readObject();
						outObj.writeObject(tetrisCanvas.data);
						outObj.flush();
						if(receivedObject instanceof TetrisData) {
							multiTetrisCanvas.data = (TetrisData)receivedObject;
						}
					}
				} catch (Exception e) { }	
			}
		}
	}
	
	private class clientHandler extends Thread {
		private Socket socket;
		private BufferedReader in;
		private PrintWriter out;
		private ObjectInputStream inObj;
		private ObjectOutputStream outObj;
		
		public clientHandler(String IP, int port) {
			try {
				socket = new Socket(IP, port);
			} catch (Exception e) { }
		}
		
		public void run() {
			System.out.println("헉run");
			try {
				in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
				out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
				inObj = new ObjectInputStream(socket.getInputStream());
				outObj = new ObjectOutputStream(socket.getOutputStream());
				
				while(true) {
					System.out.println("헉while1");
					if(true) {
						System.out.println("헉whileif1");
						out.write(1);
						out.flush();
					}
					if(in.read()==1) break;
				}
				while(true) {
					Object receivedObject = inObj.readObject();
					outObj.writeObject(tetrisCanvas.data);
					if(receivedObject instanceof TetrisData) {
						multiTetrisCanvas.data = (TetrisData)receivedObject;
					}
				}
			} catch(Exception e) { }
		}
	}
}