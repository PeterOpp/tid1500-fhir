# DCM4QI

This repository contains code and documentation related to conversion of measurements encoded in a TID 1500 DICOM file and FHIR.

## Goal 
The DCM4QI (DICOM for Quantitative Imaging) initiative works toward standardized formats to store quantitative results derived from medical imaging.
In DICOM, structured reports are used to achieve this, linking to all relevant source entities, enabling extensive provenance tracking.
Another related promising medical standard for health data exchange is [HL7 FHIR (Fast Healthcare Interoperability Resources](https://www.hl7.org/fhir/),
which can also represent measurement data, together with all kinds of EHR data, even billing-related.
Our goal refined to
* using TID1500 as the primary source for encoding measurement results, enabling full provenance tracking, and
* exposing these results also via FHIR, enabling systems that want to collect and relate image-based and other medical data (for instance for machine learning) from a single place.
This repository is about the second item, conversion of TID1500 files to FHIR and pushing them to a FHIR server.

## Links

* official [DCM4QI instructions](https://dicom4qi.readthedocs.io/en/latest/instructions/sr-tid1500/) (supercedes Gitbook)
* old DCM4QI [Gitbook](https://qiicr.gitbooks.io) with detailed Explanations of [TID1500](https://qiicr.gitbooks.io/dcmqi-guide/user_guide/sr.html)
* [dcmqi library repository](https://github.com/QIICR/dcmqi)
* [TID 1500 Reference](http://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_TID_1500) (in part 16 of the DICOM spec)
* [FHIR](https://www.hl7.org/fhir/) Reference

## Method

We did not want to start from scratch, so we considered three possible base implementations:
* `dsr2xml` from qcmtk is a commandline tool producing an XML representation.
* The TID 1500 reader from [dcmqi](https://github.com/QIICR/dcmqi) can produce a meta json file from a TID 1500 report.
* pydicom does not yet have special support for SR files, but that's WIP by Markus Herrmann at the time of writing.
For maturity and availability, we chose `dsr2xml`, and wrote a script to convert from its [XML output (link to schema)](https://github.com/InsightSoftwareConsortium/DCMTK/blob/master/dcmsr/data/dsr2xml.xsd).

We therefore just need to implement a conversion from the metadata json format to FHIR. E.g., in the following lung case both the histological subtype and either the detected mutation or unknown should be selected. 

In the 'examples/' subfolders, there are example TID 1500 SR files and expected .json files written by hand.
This expected result is a FHIR bundle containing all resources generated and ready to be uploaded to a FHIR server.
