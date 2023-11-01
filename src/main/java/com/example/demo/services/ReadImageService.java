package com.example.demo.services;

import com.example.demo.model.PatientDetails;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

public interface ReadImageService {
    ResponseEntity<String> readImage(MultipartFile file);

}
