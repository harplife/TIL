package face;

import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.Image;
import com.amazonaws.services.rekognition.model.BoundingBox;
import com.amazonaws.services.rekognition.model.CompareFacesMatch;
import com.amazonaws.services.rekognition.model.CompareFacesRequest;
import com.amazonaws.services.rekognition.model.CompareFacesResult;
import com.amazonaws.services.rekognition.model.ComparedFace;
import java.util.List;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.ByteBuffer;
import com.amazonaws.util.IOUtils;

/*
 * 
 * <!-- AWS SDK -->
 * <dependency>
 * 	<groupId>com.amazonaws</groupId>
 * 	<artifactId>aws-java-sdk</artifactId>
 * 	<version>1.11.327</version>
 * </dependency>
 * 
 * This is a java code for using AWS Face Comparison API.
 * Use the Maven above to download AWS SDK.
 * You need to login to AWS website and set up authorization..
 * follow the step by step guide, provided by Amazon:
 * https://docs.aws.amazon.com/rekognition/latest/dg/faces-comparefaces.html
 * 
 */

public class CompareFaces {

	public static void main(String[] args) {
		Float similarityThreshold = 70F;
		String sourceImage = "< PATH TO IMAGE >";
		String targetImage = "< PATH TO IMAGE >";
		ByteBuffer sourceImageBytes=null;
		ByteBuffer targetImageBytes=null;

		AmazonRekognition rekognitionClient = AmazonRekognitionClientBuilder.defaultClient();
		
	       //Load source and target images and create input parameters
	       try (InputStream inputStream = new FileInputStream(new File(sourceImage))) {
	          sourceImageBytes = ByteBuffer.wrap(IOUtils.toByteArray(inputStream));
	       }
	       catch(Exception e)
	       {
	           System.out.println("Failed to load source image " + sourceImage);
	           System.exit(1);
	       }
	       try (InputStream inputStream = new FileInputStream(new File(targetImage))) {
	           targetImageBytes = ByteBuffer.wrap(IOUtils.toByteArray(inputStream));
	       }
	       catch(Exception e)
	       {
	           System.out.println("Failed to load target images: " + targetImage);
	           System.exit(1);
	       }

	       Image source=new Image()
	            .withBytes(sourceImageBytes);
	       Image target=new Image()
	            .withBytes(targetImageBytes);

	       CompareFacesRequest request = new CompareFacesRequest()
	               .withSourceImage(source)
	               .withTargetImage(target)
	               .withSimilarityThreshold(similarityThreshold);

	       // Call operation
	       CompareFacesResult compareFacesResult=rekognitionClient.compareFaces(request);


	       // Display results
	       List <CompareFacesMatch> faceDetails = compareFacesResult.getFaceMatches();
	       for (CompareFacesMatch match: faceDetails){
	         ComparedFace face= match.getFace();
	         BoundingBox position = face.getBoundingBox();
	         System.out.println("Face at " + position.getLeft().toString()
	               + " " + position.getTop()
	               + " matches with " + match.getSimilarity().toString()
	               + "% confidence.");

	       }
	       List<ComparedFace> uncompared = compareFacesResult.getUnmatchedFaces();

	       System.out.println("There was " + uncompared.size()
	            + " face(s) that did not match");

		
		
	}//end main

}//end class
