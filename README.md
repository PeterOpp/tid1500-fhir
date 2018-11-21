# DCM4QI

This repository contains code and documentation related to our efforts to contribute to the Dicom4QI project. 

## Goal
The DCM4QI (Dicom for Quantitative Imaging) project works toward standardized formats to store quantitative results derived from medical imaging. In Dicom, structured reports are used to achieve this. However, other standards and formats do exist and can not be neglected completely. One promising medical standard for health data exchange is [FHIR](https://www.hl7.org/fhir/). As first step, we will try to achieve interoperability between the Dicom TID 1500 and FHIR DiagnosticReport and Observation resources. 

## Links

* official [DCM4QI instructions](https://dicom4qi.readthedocs.io/en/latest/instructions/sr-tid1500/) (supercedes Gitbook)
* old DCM4QI [Gitbook](https://qiicr.gitbooks.io) with detailed Explanations of [TID1500](https://qiicr.gitbooks.io/dcmqi-guide/user_guide/sr.html)
* [dcmqi library repository](https://github.com/QIICR/dcmqi)
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
Similar, the TID 1500 reader from DCM4QI can produce a meta json file from a TID 1500 report. We therefore just need to implement a conversion from the metadata json format to FHIR. o   Visualization of “Further Input Needed”. E.g., in the following lung case both the histological subtype and either the detected mutation or unknown should be selected. 

In the 'examples/dicom-to-fhir' folder, there is an example metadata.json file and example dicom dataset to generate a TID 15000 SR from. We also added an expected result, that a dicom to fhir conversion should produce. This expected result is a FHIR bundle containing all resources generated and ready to be uploaded to a FHIR server. There are still some open issues in the conversion, which are listed below: 

#### Open Issues

* **IDs:** In FHIR, each resource needs an ID. When uploading a bundle to a FHIR server, the server generates IDs for the resources in the bundle and ensures, that the references between resources within the bundle are kept consistent. From what we get in the dicoms and metadata file, we can not reference the patient resource. We can only use a loose "identifier" , which could be the Identifier in the DICOM tags, to link the generated report and observations to the patient. 

* **Algorithm:** One of the main advantages of the TID 15000 structured report is, that the method, how a measurement was produced, is encoded precisely. That means, the algorithm is identified and all parameters used by the algorithm are included. The FHIR standard does not support such a detailed description (at least not to my knowledge). In the observation resource, there is just a CodeableConcept field called 'method' to specify the method used to derive the measurement. But since this is only a coding, one could at best identify an algorithm (using what coding system?), but not the parameters.

* **Activity Sessions** The TID 15000 measurement groups involve differend identifiers: There is a **TrackingIdentifier**, which should be human readable and Identify the same physically measured subject. It does not have to be unique. (E.g: "Primary Tumor"). Aditionally, there is a **UniqueTrackingIdentifier**, which should Identify the same measured subject uniquely across time points and sessions. Futher, there is a **ActivitySession**, which is an integer, to encode the temporal order of measurements made on the same source data by at differend times. In general, the question arises, how to encode these concepts in FHIR. 
One possibility would be to use a Grouping Observation (just with code "lesion" or code "lymphnode", for example) and use the Observation.related field, to store relations to the Observations holding measurements of this specific lesion. Temporal relations can be encoded directly by the Observation.effectiveDateTime field, which, however would need a precise timepoint to be specified in the metadata.json file. 