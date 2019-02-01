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

def test_bundle_structure(dicom_file_path): 
    json_bundle = convert_sr_to_fhir_bundle(dicom_file_path)
    for entry in json_bundle["entry"]:
        assert "resource" in entry
        assert "request" in entry

def test_patient_reference_fit(dicom_file_path):
    json_bundle = convert_sr_to_fhir_bundle(dicom_file_path)
    patient_resources = get_resources_of_type(json_bundle, "Patient")
    assert len(patient_resources) == 1
    patient = patient_resources[0]
    patient_id = patient["id"]
    
    for diagnostic_report in get_resources_of_type(json_bundle, "DiagnosticReport"):
        assert diagnostic_report["subject"]["reference"] == "Patient/" + patient_id
    
    for imaging_study in get_resources_of_type(json_bundle, "ImagingStudy"):
        assert imaging_study["patient"]["reference"] == "Patient/" + patient_id

    for observation in get_resources_of_type(json_bundle, "Observation"):
        assert observation["subject"]["reference"] == "Patient/" + patient_id

def test_report_reference_fit(dicom_file_path):
    json_bundle = convert_sr_to_fhir_bundle(dicom_file_path)
    diagnostic_report_resources = get_resources_of_type(json_bundle, "DiagnosticReport")
    assert len(diagnostic_report_resources) == 1
    results = diagnostic_report_resources[0]["result"]
    observation_references = [ result["reference"] for result in results]
    
    for observation in get_resources_of_type(json_bundle, "Observation"):
        assert "Observation/" + observation["id"] in observation_references
    

def get_resources_of_type(bundle, type):
    return [ entry["resource"] for entry in bundle["entry"] if entry["resource"]["resourceType"] == type]