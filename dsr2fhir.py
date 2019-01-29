#!/usr/bin/env python
import subprocess
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description = 'Transform a DICOM SR file into a FHIR resource bundle.')
parser.add_argument('sr_filename')
args = parser.parse_args()

dcm2xml = subprocess.Popen(['dcm2xml', args.sr_filename], stdout = subprocess.PIPE)
tree = ET.parse(dcm2xml.stdout)
tree.getroot()
ET.dump(tree)
