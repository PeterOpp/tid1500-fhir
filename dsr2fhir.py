#!/usr/bin/env python
import subprocess
import argparse
import json
import xml.etree.ElementTree as ET


DEFAULT_PATIENT_ID = 'Patient'

DICOM_SEX_TO_FHIR_GENDER = {
    'M' : 'male',
    'F' : 'female',
    'O' : 'other',
    '' : 'unknown',
}

def _tag_value(root, name = None):
    tag_element = root.find(".*element[@name='%s']" % name)
    if tag_element is None:
        raise KeyError('tag named %r not found' % name)
    return tag_element.text


def patient_resource(root):
    result = dict(resourceType = 'Patient')
    result['id'] = DEFAULT_PATIENT_ID
    result['name'] = dict(
        family = _tag_value(root, 'PatientName')
    )
    result['identifier'] = dict(
        system = 'urn:dicom:<<<patient_id>>>',
        value = _tag_value(root, 'PatientID')
    )
    result['gender'] = DICOM_SEX_TO_FHIR_GENDER[_tag_value(root, 'PatientSex')]

    birthDate = _tag_value(root, 'PatientBirthDate')
    # TODO: fall back to study date minus _tag_value(root, 'PatientAge')
    
    if birthDate:
        result['birthDate'] = birthDate

    return result


def bundle(entries, default_request_method = 'POST'):
    for entry in entries:
        if not 'request' in entry:
            entry['request'] = dict(
                method = default_request_method,
                url = '')
    
    result = dict(resourceType = 'Bundle')
    result['type'] = 'transaction'
    result['entry'] = entries
    return result



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Transform a DICOM SR file into a FHIR resource bundle.')
    parser.add_argument('sr_filename')
    args = parser.parse_args()

    dcm2xml = subprocess.Popen(['dcm2xml', args.sr_filename], stdout = subprocess.PIPE)
    tree = ET.parse(dcm2xml.stdout)

    print(json.dumps(bundle([
        patient_resource(tree.getroot()),
    ])))
