package com.example.demo.services.impl;

import com.example.demo.model.Staff;
import com.example.demo.repository.PatientRepository;
import com.example.demo.repository.StaffRepository;
import com.example.demo.services.StaffService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class StaffServiceImpl implements StaffService {

    @Autowired
    StaffRepository staffRepository;
    @Override
    public Staff addStaff(Staff staff) {
        String randomId= UUID.randomUUID().toString();
        staff.setId(randomId);
        return this.staffRepository.save(staff);
    }
}
