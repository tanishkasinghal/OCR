package com.example.demo.repository;

import com.example.demo.model.PatientDetails;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PatientRepository extends JpaRepository<PatientDetails,String> {
}
