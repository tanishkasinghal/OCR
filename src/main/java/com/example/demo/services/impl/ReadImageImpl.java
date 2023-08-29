package com.example.demo.services.impl;

import com.example.demo.services.ReadImageService;
import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class ReadImageImpl implements ReadImageService {
    @Override
    public String readImage(MultipartFile file) {
        ITesseract image = new Tesseract();
        String str = null;
        try {
            // Convert MultipartFile to temporary File
            String originalFilename = file.getOriginalFilename();
            String extension="";
            if (originalFilename != null && originalFilename.contains(".")) {
                extension= originalFilename.substring(originalFilename.lastIndexOf(".") + 1);
                System.out.println("extension "+extension);
            } else {
                return "Not a Valid image "; // No valid extension found
            }

            File tempFile = File.createTempFile("temp", "." + extension);
            file.transferTo(tempFile);

            str = image.doOCR(tempFile);


            System.out.println(str);
            Pattern namePattern = Pattern.compile("Name: (.+)");
            Matcher nameMatcher = namePattern.matcher(str);
//            if (nameMatcher.find()) {
//                String name = nameMatcher.group(1);
//                System.out.println("Name: " + name);
//            }
            tempFile.delete(); // Delete the temporary file after OCR
        } catch (Exception e) {
            System.out.println("Exception " + e.getMessage());
        }
        return str;
    }
}
