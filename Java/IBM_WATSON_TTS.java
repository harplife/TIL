package com.text.speech;

//JAVA IO
import java.io.*;
import java.util.List;

//IBM Watson 
import com.ibm.watson.developer_cloud.text_to_speech.v1.TextToSpeech;
import com.ibm.watson.developer_cloud.text_to_speech.v1.model.SynthesizeOptions;
import com.ibm.watson.developer_cloud.text_to_speech.v1.util.WaveUtils;
import com.ibm.watson.developer_cloud.text_to_speech.v1.model.Voice;

/*
<!-- DEPENDENCY FOR IBM -->
<dependency>
<groupId>com.ibm.watson.developer_cloud</groupId>
<artifactId>java-sdk</artifactId>
<version>6.7.0</version>
</dependency>
 */


public class IBM_WATSON_TTS {

	public static void main(String[] args) {
		final String username = "<IBM TTS API username here>";
		final String password = "<IBM TTS API password here>";

		// IBM Watson TSS 생성
		TextToSpeech tts = new TextToSpeech();
		tts.setUsernameAndPassword(username, password);

		// IBM 음성 목록 출력
		List<Voice> list = tts.listVoices().execute().getVoices(); 
		for(Voice voice : list) {
			System.out.println(voice.getLanguage() );
			System.out.println(voice.getDescription() );
			System.out.println(voice.getName() );			
		}//end for

		// 음성 생성
		try {
			String text = "Hello wolrd jino";
			
			// 음성 생성 옵션 설정
			SynthesizeOptions SO = 
					new SynthesizeOptions.Builder().text(text).accept("audio/wav")
					.voice("en-US_AllisonVoice").build();
			
			//IBM 사이트에서 음성 전송 준비 전송 위치 ,전송형식, 전송 지점
			InputStream is = tts.synthesize(SO).execute();
			InputStream in = WaveUtils.reWriteWaveHeader(is);
			OutputStream out = new FileOutputStream("c://ibm//test_123.wav");

			//음성 전송
			byte[] buffer = new byte[8 * 1024];
			int length;
			while ( (length = in.read(buffer) ) > 0) {
				//테이트 출력
				System.out.println(length);
				out.write( buffer, 0, length);
			}
			//음성 전송 후 스트림 객체 소멸 처리
			out.close(); 			
			in.close();
			is.close();
			System.out.println("음성파일 생성 완료");
		} // end try
		catch (IOException e) {
			e.printStackTrace();
		} // end catch
		

	}// end main
}// end class
