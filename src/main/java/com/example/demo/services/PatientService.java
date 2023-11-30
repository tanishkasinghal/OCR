package com.example.demo.services;

import com.example.demo.model.PatientDetails;
import org.springframework.web.multipart.MultipartFile;

import java.io.FileNotFoundException;

public interface PatientService {
    PatientDetails addPatient(PatientDetails patient, MultipartFile file);

    PatientDetails getFile(String fileName) throws FileNotFoundException;
}
