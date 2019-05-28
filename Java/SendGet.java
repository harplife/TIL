package face;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.net.URLEncoder;

public class SendGet {

	public static void main(String[] args) throws IOException {
		String USER_AGENT = "Mozilla/5.0";

		String GET_MSG = URLEncoder.encode("김향기","UTF-8");
		String GET_URL = "http://70.12.114.189:5000/select/" + GET_MSG;
		
		URL obj = new URL(GET_URL);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();
		con.setRequestMethod("GET");
		con.setRequestProperty("User-Agent", USER_AGENT);
		int responseCode = con.getResponseCode();
		System.out.println("GET Response Code :: " + responseCode);
		if (responseCode == HttpURLConnection.HTTP_OK) { // success
			BufferedReader in = new BufferedReader(new InputStreamReader(
					con.getInputStream()));
			String inputLine;
			StringBuffer response = new StringBuffer();

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			byte[] strBytes = response.toString().getBytes("UTF-8");
			in.close();

			// print result
			String result = new String(strBytes,"UTF-8");
			System.out.println(result);
		} else {
			System.out.println("GET request not worked");
		}//end if

	}//end main

}//end class
