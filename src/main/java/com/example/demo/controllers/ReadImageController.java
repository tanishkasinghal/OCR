package com.example.demo.controllers;

import com.example.demo.model.PatientDetails;
import com.example.demo.model.Staff;
import com.example.demo.services.PatientService;
import com.example.demo.services.ReadImageService;
import com.example.demo.services.StaffService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.security.Principal;

@RestController
@RequestMapping("/ocr")
public class ReadImageController {
    @Autowired
    private ReadImageService readImageService;
    @Autowired
    private PatientService patientService;
    @Autowired
    private StaffService staffService;
//    @PostMapping("/readImage")
//    public String readImage(@RequestParam("image")MultipartFile image){
//        return readImageService.readImage(image);
//    }
    @GetMapping("/")
    public String HellowWorld(){
        return "Hello";
    }
    @PostMapping("/readImage")
    public ResponseEntity<String> readImage(@RequestParam("image")MultipartFile image){
        return readImageService.readImage(image);
    }
    @PostMapping("/")
    public ResponseEntity<PatientDetails> addPatient(@Valid @RequestBody PatientDetails patient){
        PatientDetails newEmployee=this.patientService.addPatient(patient);
        return new ResponseEntity<>(newEmployee, HttpStatus.CREATED);
    }

    @PostMapping("/addStaff")
    public ResponseEntity<Staff> addStaff(@Valid @RequestBody Staff staff){
        Staff newEmployee=this.staffService.addStaff(staff);
        return new ResponseEntity<>(newEmployee, HttpStatus.CREATED);
    }

    @GetMapping("/current-user")
    public String getLoggedInUser(Principal principal){
        return principal.getName();
    }
}
