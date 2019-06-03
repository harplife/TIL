package com.text.recog;

import java.util.List;

import com.ibm.watson.developer_cloud.service.security.IamOptions;
import com.ibm.watson.developer_cloud.visual_recognition.v3.*;
import com.ibm.watson.developer_cloud.visual_recognition.v3.model.*;

/*
<!-- DEPENDENCY FOR IBM -->
<dependency>
<groupId>com.ibm.watson.developer_cloud</groupId>
<artifactId>java-sdk</artifactId>
<version>6.7.0</version>
</dependency>
 */


public class IBM_WATSON_VR {

	public static void main(String[] args) {
		// IBM Watson 인증 정보
		final String ApiKey = "<WATSON Visual Recognition APIKEY here>";
		// VisualRecognition instance 객체 생성
		VisualRecognition VR = new VisualRecognition("2016-05-20");
		IamOptions ios = new IamOptions.Builder().apiKey(ApiKey).build();
		VR.setIamCredentials(ios);

		String URL = "https://raw.githubusercontent.com/watson-developer-cloud/"
				+ "doc-tutorial-downloads/master/visual-recognition/fruitbowl.jpg";

		// 분류 객체 생성
		ClassifyOptions cos = new ClassifyOptions.Builder().url(URL).build();

		// 분류 결과 객체에 결과값 반환 기본 반환 타입 JSON
		ClassifiedImages result = VR.classify(cos).execute();
		// 결과 반환
		System.out.println("Classification Results:");
		System.out.println(result.toString());
		System.out.println(
				result.getImages().get(0).getClassifiers().get(0).getClasses().get(0).getClassName().toString());
		System.out.println(result.getImages().get(0).getClassifiers().get(0).getClasses().get(0).getScore());

		List<ClassResult> s3 = result.getImages().get(0).getClassifiers().get(0).getClasses();

		String result2 = "";

		for (int i = 0; i < s3.size(); i++) {
			result2 += " 분석 예상 결과는 : " + s3.get(i).getClassName();
			result2 += " 분석 점수 : " + s3.get(i).getScore() + "\n ";
		} // end for

		System.out.println(result2);

	}// end main
}// endclass
