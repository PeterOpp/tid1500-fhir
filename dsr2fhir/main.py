#!/usr/bin/env python
import subprocess
import argparse
import xml.etree.ElementTree as ET
from . import resource_extractors


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

def convert_sr_to_fhir_bundle(filename):
    dsr2xml = subprocess.Popen(['dsr2xml', filename], stdout = subprocess.PIPE)
    tree = ET.parse(dsr2xml.stdout)
    root = tree.getroot()
    return bundle([
        resource_extractors.patient_resource(root),
        resource_extractors.imaging_study_resource(root),
        resource_extractors.diagnostic_report_resource(root),
    ])

def main():
    import json
    parser = argparse.ArgumentParser(description = 'Convert a DICOM SR file (TID 1500) into FHIR resources')
    parser.add_argument('sr_filename')
    args = parser.parse_args()
    print(json.dumps(convert_sr_to_fhir_bundle(args.sr_filename)))

if __name__ == '__main__':
    main()
