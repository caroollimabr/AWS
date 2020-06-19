package com.amazonaws.samples;

import java.io.File;
import java.util.List;

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ListObjectsRequest;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3ObjectSummary;


public class S3Exemplo {
	public static void main(String[] args) {
		String accessKey = "BLABLA";
		String secretKey = "blabla";
		
		BasicAWSCredentials awsCredentials = new BasicAWSCredentials(accessKey, secretKey);
		
		/*acesso ao s3*/
		AmazonS3 s3 = AmazonS3ClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(awsCredentials))
				.withRegion(Regions.US_EAST_1).build();
		
//		System.out.println("Criando bucket!");
		String bucketName = "bucket-sdk";
//		s3.createBucket(bucketName);
		
		System.out.println("listando buckets...");
		List<Bucket> buckets = s3.listBuckets();	
		for (Bucket bucket : buckets) {
			System.out.println(bucket.getName()); //mostra o bucket referente a accessKey e a secretKey
		}
		
//		System.out.println("Enviando arquivo...");
//		File file = new File("1.jpg");
//		s3.putObject(bucketName, "1.jpg", file);
		
		System.out.println("Listando objetos do bucket");
		ListObjectsRequest withBucketName = new ListObjectsRequest().withBucketName(bucketName);
		ObjectListing listObjects = s3.listObjects(withBucketName);
		for (S3ObjectSummary objectSummary : listObjects.getObjectSummaries()) {
			System.out.println("*" + objectSummary.getKey() + " - " + objectSummary.getSize() + " - " + objectSummary.getOwner());
		}
		
//		System.out.println("Deletando objeto no bucket");
//		s3.deleteObject(bucketName, "1.jpg");
		
//		System.out.println("Listando objetos do bucket...");
//		ObjectListing listObjects2 = s3.listObjects(withBucketName);
//		for (S3ObjectSummary objectSummary : listObjects.getObjectSummaries()) {
//				System.out.println("*" + objectSummary.getKey() + " - " + objectSummary.getSize());
//		}
		
		
//		s3.deleteBucket(bucketName); //deleta o bucket que foi criado
	}

}
