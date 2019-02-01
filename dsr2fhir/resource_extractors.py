'''
The methods in this module shall extract all relevant measurement
information from DICOM structured reports (specifically, TID1500
instances) and generate FHIR resources.

Useful link: dsr2xml's schema definition
https://github.com/InsightSoftwareConsortium/DCMTK/blob/master/dcmsr/data/dsr2xml.xsd
'''

import itertools

DEFAULT_PATIENT_ID = 'Patient'
DEFAULT_IMAGING_STUDY_ID = 'ImageLibrary'
DEFAULT_DIAGNOSTIC_REPORT_ID = 'DiagnosticReport'

DICOM_SEX_TO_FHIR_GENDER = {
    'M' : 'male',
    'F' : 'female',
    'O' : 'other',
    '' : 'unknown',
}


def _terminology(dcm_terminology):
    '''Return FHIR code system URI for given DICOM coding scheme designator'''
    if dcm_terminology == 'DCM':
        return 'http://dicom.nema.org/resources/ontology/DCM'
    elif dcm_terminology in ('SRT', 'SCT'): # what about 'SNM3'?
        return 'http://snomed.info/sct'
    return dcm_terminology

def _coded_concept(concept_element):
    return dict(
        coding = [dict(
            code = concept_element.find('value').text,
            display = concept_element.find('meaning').text,
            system = _terminology(concept_element.find('scheme/designator').text),
        )]
    )

def _person_name(element):
    result = dict()
    for tag_name, attribute_name in (
            ('prefix', 'prefix'),
            ('first', 'given'),
            ('middle', 'given'),
            ('last', 'family'),
            ('suffix', 'suffix'),
        ):
        child_element = element.find(tag_name)
        if child_element is not None:
            if attribute_name not in result:
                result[attribute_name] = child_element.text
            else:
                result[attribute_name] += ' ' + child_element.text
    return result


def patient_resource(root):
    patient_element = root.find('patient')
    assert patient_element is not None
    
    result = dict(resourceType = 'Patient')
    result['id'] = DEFAULT_PATIENT_ID
    result['name'] = [_person_name(patient_element.find('name'))]
    result['identifier'] = [dict(
        system = 'urn:dicom:<<<patient_id>>>',
        value = patient_element.find('id').text
    )]
    result['gender'] = DICOM_SEX_TO_FHIR_GENDER[patient_element.find('sex').text]

    birthDate = None#_tag_value(root, 'PatientBirthDate')
    # TODO: fall back to study date minus _tag_value(root, 'PatientAge')
    
    if birthDate:
        result['birthDate'] = birthDate

    return result


def imaging_study_resource(root, patient_id = DEFAULT_PATIENT_ID):
    '''Extract imaging study that was the evidence used for the
    measurement report
    '''
    
    result = dict(resourceType = 'ImagingStudy')
    result['id'] = DEFAULT_IMAGING_STUDY_ID

    study_element = root.find('evidence/study')
    result['uid'] = study_element.attrib['uid']
    result['patient'] = dict(
        reference = 'Patient/%s' % patient_id,
    )

    # this feels a little unclean, since we're looking inside the report, and
    # it may not /always/ have a 1:1 relationship with an imaging study
    result['procedureCode'] = _coded_concept(
        root.find("document/content/container/code[relationship='HAS CONCEPT MOD']/concept[value='121058']/.."))
    
#    result['started']
    serieses = []
    for series_element in study_element.findall('series'):
        series = dict()
        series['uid'] = series_element.attrib['uid']
        instances = []
        for instance_element in series_element.findall('value'):
            instances.append(dict(
                sopClass = instance_element.find('sopclass').text,
                uid = instance_element.find('instance').attrib['uid'],
            ))
        if instances:
            series['instance'] = instances
        serieses.append(series)
    if serieses:
        result['series'] = serieses
    
    return result


def observation_groups_resources(measurement_group_element, observation_counter, report_status):
    result = []
    group_observation = dict(resourceType = 'Observation')
    group_observation['id'] = 'Observation%d' % next(observation_counter)
    result.append(group_observation)
    # in DICOM, measurement groups do not have a status themselves:
    group_observation['status'] = dict(partial = 'preliminary', final = 'final')[report_status]
    return result


def diagnostic_report_resources(
        root,
        imaging_study_id = DEFAULT_IMAGING_STUDY_ID,
        patient_id = DEFAULT_PATIENT_ID):
    result = []
    
    report = dict(resourceType = 'DiagnosticReport')
    report['id'] = DEFAULT_DIAGNOSTIC_REPORT_ID
    result.append(report)
    
    report['identifier'] = [dict(
        system = 'urn:dicom:uid',
        value = root.find('instance').attrib['uid'],
    )]

    container_element = root.find('document/content/container')
    
    concept_element = container_element.find('concept')
    report['code'] = _coded_concept(concept_element)

    # possible FHIR status values:   registered | partial | preliminary | final
    # amended | corrected | appended | cancelled | entered-in-error | unknown

    status = 'unknown'
    completion_element = root.find('document/completion')
    if completion_element is not None:
        status = dict(PARTIAL = 'partial', COMPLETE = 'final')[
            completion_element.attrib['flag']]
    report['status'] = status
    
    report['subject'] = dict(
        reference = 'Patient/%s' % patient_id,
    )
    report['imagingStudy'] = [
        dict(reference = 'ImagingStudy/%s' % imaging_study_id),
    ]

    performers = []
    for pname_element in container_element.findall("pname/concept[value='121008']/.."):
        # Person Observer Name
        performers.append(dict(
            actor = _person_name(pname_element.find('value')),
        ))
    report['performer'] = performers

    observation_counter = itertools.count(1)
    
    observations = []
    # we focus on 126010 / "Imaging Measurements" for now
    # (there are also "Derived Imaging Measurements" and "Qualitative Evaluations"
    measurements_element = container_element.find("container[relationship='CONTAINS']/concept[value='126010']/..")
    for measurement_group_element in measurements_element.findall(
            "container[relationship='CONTAINS']/concept[value='125007']/.."):
        observations.extend(
            observation_groups_resources(
                measurement_group_element,
                observation_counter,
                report_status = report['status']))
    
    results = []
    for observation in observations:
        results.append(dict(reference = 'Observation/%s' % observation['id']))
    report['result'] = results
    
    result.extend(observations)
    return result


