package Tetris;

import java.awt.EventQueue;
import java.io.*;
import java.net.*;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import java.awt.BorderLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class MyClient extends JFrame {
	
	private Socket socket = null;
	private ObjectOutputStream out = null;
	private ObjectInputStream in = null;

	private JPanel contentPane;
	public static TetrisCanvas tetrisCanvas, tetrisCanvas_1;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MyClient frame = new MyClient("127.0.0.1", 30000);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public MyClient(String IP, int port) {
		renderUI();
		try {
			socket = new Socket(IP, port);
		} catch (Exception e) { }
	}

	private void renderUI() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 700, 600);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		JMenu mnNewMenu = new JMenu("게임");
		menuBar.add(mnNewMenu);
		
		JMenuItem mntmNewMenuItem = new JMenuItem("시작");
		mntmNewMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				tetrisCanvas.start();
				mntmNewMenuItem.setEnabled(false);
			}
		});
		
		mnNewMenu.add(mntmNewMenuItem);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(new BorderLayout(0, 0));
		
		tetrisCanvas = new TetrisCanvas();
		contentPane.add(tetrisCanvas, BorderLayout.CENTER);
		tetrisCanvas.setLayout(null);
		
		tetrisCanvas_1 = new TetrisCanvas();
		contentPane.add(tetrisCanvas_1, BorderLayout.EAST);
		tetrisCanvas_1.setLayout(null);
	}
}
