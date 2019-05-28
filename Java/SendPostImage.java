package face;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Base64;
import javax.imageio.ImageIO;

/*
 * Maybe not the best way, but one way to send POST Request with Java
 */

public class SendPostImage {

	public static void main(String[] args) throws IOException {
//		TEST 1 : SENDING STRING, ENCODED AS BASE64
		String originalInput = "text";
		String encodedString = Base64.getEncoder().encodeToString(originalInput.getBytes());
		// print byte string of the word
		System.out.println(encodedString);
		byte[] decodedBytes = Base64.getDecoder().decode(encodedString);
		String decodedString = new String(decodedBytes);
		// decode the bytes and print the word
		System.out.println(decodedString);
		
//		TEST 2: SENDING IMAGE, ENCODED AS BASE64
		BufferedImage image = ImageIO.read(new File("< PATH TO IMAGE GOES HERE >"));
		ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
		ImageIO.write(image, "jpg", outputStream);
		String encodedImage = Base64.getEncoder().encodeToString(outputStream.toByteArray());
		// probably not the best idea to actually print out the bytes of an image file
//		System.out.println(encodedImage);
		
		// Just a little addition here, since dealing with encoding is always so fun
		String name = URLEncoder.encode("김향기","UTF-8");
		String POST_URL = "http://192.168.1.0:5000/update/dataset?name=" + name;
		System.out.println(POST_URL);
		
		// toggle between TEST 1 and TEST 2.
//		String POST_PARAMS = encodedString;
		String POST_PARAMS = encodedImage;
		
		URL obj = new URL(POST_URL);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();
		con.setRequestMethod("POST");
		String USER_AGENT = "Mozilla/5.0";
		con.setRequestProperty("User-Agent", USER_AGENT);

		// For POST only - START
		con.setDoOutput(true);
		OutputStream os = con.getOutputStream();
		os.write(POST_PARAMS.getBytes());
		os.flush();
		os.close();
		// For POST only - END

		int responseCode = con.getResponseCode();
		System.out.println("POST Response Code :: " + responseCode);

		/*
		 * In order to test out the POST request,
		 * I built a Rest API to return either JSON or IMAGE
		 */
		if (responseCode == HttpURLConnection.HTTP_OK) { //success

			// for image processing
//		    InputStream is = new BufferedInputStream(con.getInputStream());
//		    Image response_image = ImageIO.read(is);
//		    ImageIO.write((RenderedImage) response_image, "jpg", 
//		    		new File("< filename >"));
		    
		    // for getting json
			BufferedReader in = new BufferedReader(new InputStreamReader(
			con.getInputStream()));
			String inputLine;
			StringBuffer response = new StringBuffer();

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();

			// print result
			System.out.println(response.toString());
			
		} else {
			System.out.println("POST request did not work");
		}//end if

	}//end main

}//end get
