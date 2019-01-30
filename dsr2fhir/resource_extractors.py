'''
The methods in this module shall extract all relevant measurement
information from DICOM structured reports (specifically, TID1500
instances) and generate FHIR resources.
'''

DEFAULT_PATIENT_ID = 'Patient'
DEFAULT_IMAGING_STUDY_ID = 'ImagingStudy'
DEFAULT_DIAGNOSTIC_REPORT_ID = 'DiagnosticReport'

DICOM_SEX_TO_FHIR_GENDER = {
    'M' : 'male',
    'F' : 'female',
    'O' : 'other',
    '' : 'unknown',
}


def _person_name(element):
    result = dict()
    for tag_name, attribute_name in (
            ('last', 'family'), # TODO: which other tags can dsr2xml output?
        ):
        child_element = element.find(tag_name)
        if child_element is not None:
            result[attribute_name] = child_element.text
    return result


def patient_resource(root):
    patient_element = root.find('patient')
    assert patient_element is not None
    
    result = dict(resourceType = 'Patient')
    result['id'] = DEFAULT_PATIENT_ID
    result['name'] = _person_name(patient_element.find('name'))
    result['identifier'] = dict(
        system = 'urn:dicom:<<<patient_id>>>',
        value = patient_element.find('id').text
    )
    result['gender'] = DICOM_SEX_TO_FHIR_GENDER[patient_element.find('sex').text]

    birthDate = None#_tag_value(root, 'PatientBirthDate')
    # TODO: fall back to study date minus _tag_value(root, 'PatientAge')
    
    if birthDate:
        result['birthDate'] = birthDate

    return result


def imaging_study_resource(root):
    result = dict(resourceType = 'imagingStudy')
    result['id'] = DEFAULT_IMAGING_STUDY_ID

#    result['uid'] = _tag_value(root, '###')
    
    return result


def diagnostic_report_resource(root):
    result = dict(resourceType = 'DiagnosticReport')
    result['id'] = DEFAULT_DIAGNOSTIC_REPORT_ID

    result['uid'] = root.find('instance').attrib['uid']
    
    return result


