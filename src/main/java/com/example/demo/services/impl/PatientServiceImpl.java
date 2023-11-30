package com.example.demo.services.impl;

import com.example.demo.config.FileStorageException;
import com.example.demo.model.PatientDetails;
import com.example.demo.repository.PatientRepository;
import com.example.demo.services.PatientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Objects;
import java.util.UUID;

@Service
public class PatientServiceImpl implements PatientService {
    @Autowired
    PatientRepository patientRepository;
    @Override
    public PatientDetails addPatient(PatientDetails patient, MultipartFile file) {
        String randomDepId= UUID.randomUUID().toString();
        patient.setId(randomDepId);
        String fileName = StringUtils.cleanPath(Objects.requireNonNull(file.getOriginalFilename()));

        try {
            // Check if the file's name contains invalid characters
            if (fileName.contains("..")) {
                throw new FileStorageException("Sorry! Filename contains invalid path sequence " + fileName);
            }
            patient.setData(file.getBytes());
        } catch (IOException ex) {
            throw new FileStorageException("Could not store file " + fileName + ". Please try again!", ex);
        }

        System.out.println("file name"+file.getName());
        return this.patientRepository.save(patient);
    }

    @Override
    public PatientDetails getFile(String id) throws FileNotFoundException {
        return patientRepository.findById(id)
                .orElseThrow(()-> new FileNotFoundException("File not found with id " + id));
    }
}
