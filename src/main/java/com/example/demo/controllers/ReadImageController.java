package com.example.demo.controllers;
import com.example.demo.model.PatientDetails;
import com.example.demo.services.PatientService;
import com.example.demo.services.ReadImageService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.FileNotFoundException;
import java.security.Principal;

@RestController
@RequestMapping("/ocr")
public class ReadImageController {
    @Autowired
    private ReadImageService readImageService;
    @Autowired
    private PatientService patientService;

    @GetMapping("/")
    public String HellowWorld(){
        return "Hello";
    }
    @PostMapping("/readImage")
    public ResponseEntity<String> readImage(@RequestParam("image") MultipartFile image){
        return readImageService.readImage(image);
    }
    @PostMapping("/")
    public ResponseEntity<PatientDetails> addPatient(@RequestParam("jsonData") String jsonData,@RequestParam("image")MultipartFile image) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        PatientDetails patient = objectMapper.readValue(jsonData, PatientDetails.class);
        PatientDetails newEmployee=this.patientService.addPatient(patient,image);
        return new ResponseEntity<>(newEmployee, HttpStatus.CREATED);
    }

    @GetMapping("/downloadFile/{id}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String id) throws FileNotFoundException {
        // Load file as Resource
        PatientDetails patientDetails = patientService.getFile(id);
        ByteArrayResource resource = new ByteArrayResource(patientDetails.getData());
        HttpHeaders headers = new HttpHeaders();
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + patientDetails.getId() + "\"");

        return ResponseEntity
                .ok()
                .headers(headers)
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(resource);
    }


    @GetMapping("/current-user")
    public String getLoggedInUser(Principal principal){
        return principal.getName();
    }
}
