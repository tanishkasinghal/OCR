package com.example.demo.services;

import org.springframework.web.multipart.MultipartFile;

public interface ReadImageService {
    String readImage(MultipartFile file);
}
