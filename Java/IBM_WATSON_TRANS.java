package kr.co.tran;

import com.ibm.watson.developer_cloud.language_translator.v3.LanguageTranslator;
import com.ibm.watson.developer_cloud.language_translator.v3.model.IdentifiableLanguages;
import com.ibm.watson.developer_cloud.language_translator.v3.model.IdentifiedLanguages;
import com.ibm.watson.developer_cloud.language_translator.v3.model.IdentifyOptions;
import com.ibm.watson.developer_cloud.language_translator.v3.model.TranslateOptions;
import com.ibm.watson.developer_cloud.language_translator.v3.model.TranslationModels;
import com.ibm.watson.developer_cloud.language_translator.v3.model.TranslationResult;
import com.ibm.watson.developer_cloud.service.security.IamOptions;

/*
<!-- DEPENDENCY FOR IBM -->
<dependency>
<groupId>com.ibm.watson.developer_cloud</groupId>
<artifactId>java-sdk</artifactId>
<version>6.7.0</version>
</dependency>
 */

public class IBM_WATSON_TRANS {

	public static void main(String[] args) {

		// 번역할 문장
		String text = "I know the times are difficult. "
				+ "Our sales have been  disappointing for the past three quarters for our data analytics product suite. "
				+ "We have a competitive data analytics product suite in the industry."
				+ "But we need to do our job selling it!  " + "We need to acknowledge and fix our sales challenges. "
				+ "We can't blame the economy for our lack of execution! "
				+ "We are missing critical sales opportunities.  "
				+ "Our product is in no way inferior to the competitor products."
				+ "Our clients are hungry for analytical tools to improve their  business outcomes. "
				+ "Economy has nothing to do with it. ";
		// 번역 옵션
		String ops = "en-ko";
		// IBM Watson apikey 인증값
		String apikey = "<IBM Watson Translation APIKEY here>";
		// 인증 객체 생성
		IamOptions IO = new IamOptions.Builder().apiKey(apikey).build();
		// IBM Watson 번역 객체 생성
		LanguageTranslator LT = new LanguageTranslator("2018-05-01", IO);

		
		// 사용가능 번역모델 리스트 출력
		TranslationModels models = LT.listModels().execute();
		System.out.println(models);
		
		// 문자열 언어 분석
		IdentifyOptions identifyOptions = new IdentifyOptions.Builder()
				.text(text)
				.build();
		
		IdentifiedLanguages identifiedLangs = LT.identify(identifyOptions).execute();
		System.out.println(identifiedLangs);
		
		// IBM Watson 번역 옵션 객체 생성 번역할값 번역 옵션
		TranslateOptions TO = new TranslateOptions.Builder().addText(text).modelId(ops).build();
		// 번역 결과 객체 생성
		TranslationResult result = LT.translate(TO).execute();

		// 번역 결과 일부분만 가져오기
		System.out.println(result.getWordCount());
		System.out.println(result.getCharacterCount());
		System.out.println(result.getTranslations());

	}// end main

}// end class
