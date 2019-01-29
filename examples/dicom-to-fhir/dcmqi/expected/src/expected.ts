import {
  fhirBundle,
  fhirPatient,
  fhirDiagnosticReport,
  fhirObservation,
  fhirImagingStudy
} from "./fhir-interfaces";

const diagnosticReport: fhirDiagnosticReport = {
  resourceType: "DiagnosticReport",
  status: "final",
  identifier: [{
    // this is the SOPInstanceUID and can be used to check for existing FHIR
    // representations during import of SR
    system: "urn:dicom:uid",
    value: "1.2.276.0.7230010.3.1.4.8323329.5607.1542879484.507970"
  }],
  code: {
    coding: [
      {
        code: "",
        system: "",
        display: "Imaging Measurement Report"
      }
    ]
  },
  subject: {
    reference: "Patient/Patient"
  },
  imagingStudy: [{
    reference: "ImagingStudy/ImageLibray"
  }],
  result: [
    {
      reference: "Observation/Observation_volume"
    },
    {
      reference: "Observation/Observation_attenuation_coefficient"
    }
  ]
};

const patient: fhirPatient = {
  id: "Patient",
  identifier: [{
    system: "",
    value: "99000"
  }],
  resourceType: "Patient",
  name: [{
    family: "JANCT000"
  }],
  gender: "male",
  birthDate: "1943" // inferred from age & study year
}

const imagingLibrary: fhirImagingStudy = {
  id: "ImageLibrary",
  resourceType: "ImagingStudy",
  uid: "1.2.392.200103.20080913.113635.0.2009.6.22.21.43.10.22941.1",
  patient: {
    reference: "Patient/Patient"
  },
  modalityList: [
    {
      system: "DCM",
      code: "CT",
      display: "Computed Tomography"
    }
  ],
  started: "2003-04-17 10:46:07",
  series: [
    {
      uid: "1.2.392.200103.20080913.113635.1.2009.6.22.21.43.10.23430.1",
      modality: {
        code: "CT",
        system: "DCM",
        display: "Computed Tomography"
      },
      instance: [
        {
          sopClass: "CTImageStorage",
          uid: "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23431.1"
        },
        {
          sopClass: "CTImageStorage",
          uid: "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23432.1"
        },
        {
          sopClass: "CTImageStorage",
          uid: "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23433.1"
        }
      ]
    }
  ]
};


const observation_attenuation_coefficient: fhirObservation = {
  resourceType: "Observation",
  id: "Observation_attenuation_coefficient",
  status: "final",
  bodySite: {
    coding: [
      {
        code: "T-62000",
        system: "SRT",
        display: "Liver"
      }
    ]
  },
  method: {
    coding: [
      // Coding and Algorithm are not exactly interchangeable
    ]
  },
  code: {
    coding: [
      {
        code: "112031",
        system: "DCM",
        display: "Attenuation Coefficient"
      }
    ]
  },
  component: [
    {
      code: {
        coding: [
          {
            system: "SRT",
            code: "R-00317",
            display: "Mean"
          }
        ]
      },
      valueQuantity: {
        value: 37.3289,
        system: "UCUM",
        code: "[hnsf'U]",
        unit: "Hounsfield unit"
      }
    },
    {
      code: {
        coding: [
          {
            system: "SRT",
            code: "R-404FB",
            display: "Minimum"
          }
        ]
      },
      valueQuantity: {
        value: -778,
        system: "UCUM",
        code: "[hnsf'U]",
        unit: "Hounsfield unit"
      }
    },
    {
      code: {
        coding: [
          {
            system: "SRT",
            code: "G-A437",
            display: "Maximum"
          }
        ]
      },
      valueQuantity: {
        value: 221,
        system: "UCUM",
        code: "[hnsf'U]",
        unit: "Hounsfield unit"
      }
    },
    {
      code: {
        coding: [
          {
            system: "SRT",
            code: "R-10047",
            display: "Standard Deviation"
          }
        ]
      },
      valueQuantity: {
        value: 59.1691,
        system: "UCUM",
        code: "[hnsf'U]",
        unit: "Hounsfield unit"
      }
    }
  ]
};

const observation_volume: fhirObservation = {
  resourceType: "Observation",
  id: "Observation_volume",
  status: "final",
  bodySite: {
    coding: [
      {
        code: "T-62000",
        system: "SRT",
        display: "Liver"
      }
    ]
  },
  method: {
    coding: [
      // Coding and Algorithm are not exactly interchangeable
    ]
  },
  code: {
    coding: [
      {
        code: "G-D705",
        system: "SRT",
        display: "Volume"
      }
    ]
  },
  valueQuantity: {
    value: 70361.9,
    system: "UCUM",
    code: ".m3",
    unit: "Cubic millimeter"
  }
};

const request = {
  method: "POST",
  url: ""
};

export const bundle: fhirBundle = {
  resourceType: "Bundle",
  type: "transaction",
  entry: [
    {
      resource: diagnosticReport,
      request: request
    },
    {
      resource: patient,
      request: request
    },
    {
      resource: observation_attenuation_coefficient,
      request: request
    },
    {
      resource: observation_volume,
      request: request
    },
    {
      resource: imagingLibrary,
      request: request
    }
  ]
};
