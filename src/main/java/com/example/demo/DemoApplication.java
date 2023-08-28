package com.example.demo;

import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.File;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
//		ITesseract image=new Tesseract();
//		String str= null;
//		try {
//			str = image.doOCR(new File("/home/tanishka/Documents/PE/testocr.png"));
//			System.out.println("Data From image is "+str);
//		} catch (TesseractException e) {
//			System.out.println("Exception "+e.getMessage());
//		}
	}

}
