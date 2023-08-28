package com.example.demo.controllers;

import com.example.demo.services.ReadImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/read")
public class ReadImageController {
    @Autowired
    private ReadImageService readImageService;
    @PostMapping("/image")
    public String readImage(@RequestParam("image")MultipartFile image){
        return readImageService.readImage(image);
    }
}
