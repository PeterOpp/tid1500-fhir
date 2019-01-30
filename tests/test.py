import os
import sys
import pytest
import json
from dsr2fhir.main import convert_sr_to_fhir_bundle
from json_compare import json_compare

TestCasesExpected = [
    "examples/dcmqi/expected.json",
    "examples/rsna2018_dataset1/expected.json"
]

TestCasesPaths = [
    "examples/dcmqi/result.dcm",
    "examples/rsna2018_dataset1/sr-tid1500-ct-liver-example.dcm"
]


@pytest.fixture(params=TestCasesPaths)
def dicom_file_path(request):
    return request.param


@pytest.fixture(params=TestCasesExpected)
def expected_bundle(request):
    file = open(request.param, "r")
    return file.read()


def test_conversion_produces_json(dicom_file_path):
    json_bundle = convert_sr_to_fhir_bundle(dicom_file_path)
    assert type(json_bundle) is dict


def test_json_equals_except_ids(dicom_file_path, expected_bundle):
    json_bundle = convert_sr_to_fhir_bundle(dicom_file_path)
    expected_json = json.loads(expected_bundle)
    result = json_compare.are_same(expected_json, json_bundle, True, ["reference", "id"])
    print(result)
    assert result[0]
