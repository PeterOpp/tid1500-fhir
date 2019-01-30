import os,sys
import pytest
from dsr2fhir import *

TestCasesExpected = [
  "examples/dcmqi/expected/expected_result.json",
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
  jsonBundle = convertSrToJsonBundle(dicomFilePath)
  assert type(jsonBundle) is dict

