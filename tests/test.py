import os,sys
import pytest
from dsr2fhir.main import convert_sr_to_fhir_bundle

TestCasesExpected = [
  "examples/dcmqi/expected.json",
  "examples/rsna2018_dataset1/expected.json"
]

TestCasesPaths = [
  "examples/dcmqi/result.dcm",
  "examples/rsna2018_dataset1/sr-tid1500-ct-liver-example.dcm"
]

@pytest.fixture(params=TestCasesPaths )
def dicomFilePath( request ):
  return request.param

def test_conversion_produces_json(dicomFilePath):
  jsonBundle = convert_sr_to_fhir_bundle(dicomFilePath)
  assert type(jsonBundle) is dict

