package com.example.demo.services.impl;

import com.example.demo.model.PatientDetails;
import com.example.demo.services.ReadImageService;
import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class ReadImageImpl implements ReadImageService {
    @Override
    public ResponseEntity<String> readImage(MultipartFile file) {
        ITesseract image = new Tesseract();
        try {
            // Convert MultipartFile to temporary File
            String originalFilename = file.getOriginalFilename();
            String extension="";
            if (originalFilename != null && originalFilename.contains(".")) {
                extension= originalFilename.substring(originalFilename.lastIndexOf(".") + 1);
                System.out.println("extension "+extension);
            } else {
                return ResponseEntity.badRequest().body("Not a Valid imagee");
            }


            String apiUrl = "http://localhost:5000/upload"; // Replace with your Python API URL
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", file.getResource());

            ResponseEntity<String> response = new RestTemplate().postForEntity(apiUrl, body, String.class);
            System.out.println(response.toString());
            if (response.getStatusCode().is2xxSuccessful()) {
                return response;
            } else {
                return ResponseEntity.badRequest().body("Not a Valid image");
            }
//
//            File tempFile = File.createTempFile("temp", "." + extension);
//            file.transferTo(tempFile);
//            str=file.toString();
//            str = image.doOCR(tempFile);
//
//
//            System.out.println(str);
//            Pattern namePattern = Pattern.compile("Name: (.+)");
//            Matcher nameMatcher = namePattern.matcher(str);
//            if (nameMatcher.find()) {
//                String name = nameMatcher.group(1);
//                System.out.println("Name: " + name);
//            }
//            tempFile.delete(); // Delete the temporary file after OCR
        } catch (Exception e) {
            System.out.println("Exception " + e.getMessage());
        }
        return ResponseEntity.badRequest().body("Not a Valid image");
    }

}
