#!/usr/bin/env python
import subprocess
import argparse
import xml.etree.ElementTree as ET
from . import resource_extractors


def bundle(resources, default_request_method = 'POST'):
    result = dict(resourceType = 'Bundle')
    result['type'] = 'transaction'
    result['entry'] = []
    
    for resource in resources:
        result['entry'].append(dict(
            request = dict(
                method = default_request_method,
                url = ''),
            resource = resource))
    
    return result

def _dsr2xml(filename):
    dsr2xml = subprocess.Popen(['dsr2xml', filename], stdout = subprocess.PIPE)
    # TODO: error handling
    tree = ET.parse(dsr2xml.stdout)
    return tree

def convert_sr_to_fhir_bundle(filename):
    tree = _dsr2xml(filename)
    root = tree.getroot()
    return bundle(
        resource_extractors.diagnostic_report_resources(root) + [
        resource_extractors.patient_resource(root),
        resource_extractors.imaging_study_resource(root),
    ])

def main():
    import json
    parser = argparse.ArgumentParser(description = 'Convert a DICOM SR file (TID 1500) into FHIR resources')
    parser.add_argument('sr_filename')
    args = parser.parse_args()
    print(json.dumps(convert_sr_to_fhir_bundle(args.sr_filename)))

if __name__ == '__main__':
    main()
