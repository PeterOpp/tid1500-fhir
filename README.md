# DCM4QI

This repository contains code and documentation related to our efforts to contribute to the Dicom4QI project. 

## Goal
The DCM4QI (Dicom for Quantitative Imaging) project works toward standardized formats to store quantitative results derived from medical imaging. In Dicom, structured reports are used to achieve this. However, other standards and formats do exist and can not be neglected completely. One promising medical standard for health data exchange is [FHIR](https://www.hl7.org/fhir/). As first step, we will try to achieve interoperability between the Dicom TID 1500 and FHIR DiagnosticReport and Observation resources. 

## Links

* DCM4QI [Gitbook](https://qiicr.gitbooks.io) with detailed Explanations of [TID1500](https://qiicr.gitbooks.io/dcmqi-guide/user_guide/sr.html)
* DCM4QI [Repository](https://github.com/QIICR/dcmqi)
* TID 1500 [Reference](http://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_TID_1500)
* [FHIR](https://www.hl7.org/fhir/) Reference

## Method

### FHIR to Dicom
The DCM4QI project offers a TID 1500 writer, that is able to produce a dcm-file that contains a Measurement Report using: 
* a set of source dicom files for populating the "Image Library" in the Measurement Report
* a set of source dicom files for populating the "composite context" in the Measurement Report
* a [metadata file](https://github.com/QIICR/dcmqi/blob/master/doc/schemas/sr-tid1500-schema.json), containing the actual measurements

Therefore, to provide a conversion from FHIR to TID 1500, we just need to generate the metadata json file and identify the correct DICOM images related. The rest is already implemented in the TID 1500 writer. 

### DICOM to FHIR
Similar, the TID 1500 reader from DCM4QI can produce a meta json file from a TID 1500 report. We therefore just need to implement a conversion from the metadata json format to FHIR. 
