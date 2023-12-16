import java.io.BufferedInputStream;
import java.io.InputStream;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.FloatControl;
import javax.sound.sampled.LineEvent;
import javax.sound.sampled.LineListener;

public class SoundHandler {
	private Clip clip;
	FloatControl gainControl;
	
	float volume = 0.8f;
	
	public SoundHandler(String filename) { // 사운드를 설정한다.
	    try {
	        InputStream inputStream = getClass().getResourceAsStream(filename);
	        
	        // AudioSystem으로부터 새로운 Clip 객체를 얻는다.
	        clip = AudioSystem.getClip();

	        // LineListener를 추가하여 사운드가 정지될 때 이벤트를 처리한다.
	        clip.addLineListener(new LineListener() {
	            @Override
	            public void update(LineEvent event) {
	                if (event.getType() == LineEvent.Type.STOP) {
	                    try {
	                        // 현재 재생 중인 사운드를 닫고
	                        clip.close();
	                        
	                        // 새로운 InputStream을 생성하여 사운드 파일을 읽어온다.
	                        InputStream newInputStream = getClass().getResourceAsStream(filename);
	                        
	                        // 새로운 AudioInputStream을 얻어 새로운 사운드 파일을 열고 시작한다.
	                        AudioInputStream newAudioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(newInputStream));
	                        clip.open(newAudioInputStream);
	                        
	                    } catch (Exception e) {
	                        e.printStackTrace();
	                    }
	                }
	            }
	        });

	        // 처음에는 재생하지 않고, 사운드 파일을 열어둔다.
	        AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(inputStream));
	        clip.open(audioInputStream);
	        
	        // FloatControl을 여기서 얻어 마스터 게인(볼륨)을 조절할 수 있도록 한다.
	        gainControl = (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
	    } catch (Exception e) {
	        e.printStackTrace();
	    }
	}

    public void controlSound(float volume) { // 소리를 조절한다.
    	this.volume = volume;
        if (gainControl != null) {
            // 볼륨 조절
            float minVolume = gainControl.getMinimum();
            float maxVolume = gainControl.getMaximum();
            float range = maxVolume - minVolume;
            float scaledVolume = (range * volume) + minVolume;
            gainControl.setValue(scaledVolume);
        }
    }
    
    public void play() { // 사운드를 한 번 재생한다.
        try {
            if (clip != null) {
                clip.setMicrosecondPosition(0); // 재생 위치를 처음으로 설정
                clip.start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public void playLoop() { // 사운드를 반복 재생한다.
        try {
            if (clip != null) {
                clip.setMicrosecondPosition(0); // 재생 위치를 처음으로 설정
                clip.loop(Clip.LOOP_CONTINUOUSLY); // 무한 반복
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public void stop() { // 사운드 재생을 멈춘다.
        try {
            if (clip != null && clip.isRunning()) {
                clip.stop();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public void changeSound(String filename) { // 사운드를 변경한다.
        try {
            if (clip != null && clip.isRunning()) {
                clip.stop(); // 현재 재생 중인 사운드를 중지
                clip.close(); // 현재 재생 중인 사운드의 리소스를 해제
                clip = null; // clip 초기화
            }
            
            InputStream inputStream = getClass().getResourceAsStream(filename);
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(inputStream));
            clip = AudioSystem.getClip(); // clip 생성
            clip.open(audioInputStream); // 새로운 사운드 파일 열기
            clip.setMicrosecondPosition(0); // 재생 위치를 처음으로 설정
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}