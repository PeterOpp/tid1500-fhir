import os,sys
import pytest
from dsr2fhir import *

TestCasesExpected = [
  "examples/dicom-to-fhir/dcmqi/expected/expected_result.json",
  "examples/dicom-to-fhir/rsna2018_dataset1/expected.json"
]

TestCasesPaths = [
  "examples/dicom-to-fhir/dcmqi/result.dcm",
  "examples/dicom-to-fhir/rsna2018_dataset1/sr-tid1500-ct-liver-example.dcm"
]

@pytest.fixture(params=TestCasesPaths )
def dicomFilePath( request ):
  return request.param

def test_conversion_produces_json(dicomFilePath):
  jsonBundle = convertSrToJsonBundle(dicomFilePath)
  assert type(jsonBundle) is dict

