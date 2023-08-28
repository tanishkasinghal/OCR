package com.example.demo.services.impl;

import com.example.demo.services.ReadImageService;
import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;

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
            System.out.println("Data From image is " + str);

            tempFile.delete(); // Delete the temporary file after OCR
        } catch (Exception e) {
            System.out.println("Exception " + e.getMessage());
        }
        return str;
    }
}
