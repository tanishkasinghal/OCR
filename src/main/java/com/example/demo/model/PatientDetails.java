package com.example.demo.model;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name="patient")
public class PatientDetails {
    @Id
    @Column(name = "id")
    private String id;

    @Column(name = "name")
    private String name;

    @Column(name = "age")
    private String age;

    @Column(name = "date_of_birth")
    private String date_of_birth;

    @Column(name = "contact")
    private String contact;

    @Column(name = "sex")
    private String sex;

    @Column(name = "address")
    private String address;

    @Lob
    @Column(name = "prescription", columnDefinition = "LONGBLOB")
    private byte[] data;

}
