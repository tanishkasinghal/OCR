package com.example.demo.services.impl;

import com.example.demo.model.PatientDetails;
import com.example.demo.repository.PatientRepository;
import com.example.demo.services.PatientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class PatientServiceImpl implements PatientService {
    @Autowired
    PatientRepository patientRepository;
    @Override
    public PatientDetails addPatient(PatientDetails patient) {
        String randomDepId= UUID.randomUUID().toString();
        patient.setId(randomDepId);
        return this.patientRepository.save(patient);
    }
}
