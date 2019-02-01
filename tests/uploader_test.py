import pytest
import requests
import json
from dsr2fhir.resource_uploader import BundleUploader


mocked_patient_available_json = r'''{
  "resourceType": "Bundle",
  "id": "1d49f239-2e05-4e99-8097-75c57a0c3636",
  "meta": {
    "lastUpdated": "2019-01-31T16:55:11.380+00:00"
  },
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "http://localhost:8080/baseDstu3/Patient?_format=json&identifier=urn%3Adicom%3A%3C%3C%3Cpatient_id%3E%3E%3E%7C99000"
    }
  ],
  "entry": [
    {
      "fullUrl": "http://localhost:8080/baseDstu3/Patient/8803",
      "resource": {
        "resourceType": "Patient",
        "id": "8803",
        "meta": {
          "versionId": "1",
          "lastUpdated": "2019-01-31T15:48:25.995+00:00"
        },
        "text": {
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\"><b>JANCT000 </b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>99000</td></tr></tbody></table></div>"
        },
        "identifier": [
          {
            "system": "urn:dicom:<<<patient_id>>>",
            "value": "99000"
          }
        ],
        "name": [
          {
            "family": "JANCT000"
          }
        ],
        "gender": "male"
      },
      "search": {
        "mode": "match"
      }
    }
  ]
}'''

mocked_patient_available_return = r'{"resourceType": "Bundle", "type": "transaction", "entry": [{"request": {"method": "POST", "url": ""}, "resource": {"resourceType": "DiagnosticReport", "id": "DiagnosticReport", "identifier": [{"system": "urn:dicom:uid", "value": "1.2.276.0.7230010.3.1.4.0.83735.1480019874.480726"}], "code": {"coding": [{"code": "126000", "display": "Imaging Measurement Report", "system": "http://dicom.nema.org/resources/ontology/DCM"}]}, "status": "final", "subject": {"reference": "Patient/Patient"}, "imagingStudy": [{"reference": "ImagingStudy/ImageLibrary"}], "performer": [{"actor": {"family": "Reader1"}}]}}, {"request": {"method": "POST", "url": ""}, "resource": {"resourceType": "Patient", "id": "Patient", "name": [{"family": "JANCT000"}], "identifier": [{"system": "urn:dicom:<<<patient_id>>>", "value": "99000"}], "gender": "male"}}, {"request": {"method": "POST", "url": ""}, "resource": {"resourceType": "ImagingStudy", "id": "ImageLibrary", "uid": "1.2.392.200103.20080913.113635.0.2009.6.22.21.43.10.22941.1", "patient": {"reference": "Patient/Patient"}, "series": [{"uid": "1.2.276.0.7230010.3.1.3.0.42154.1458337731.665795", "instance": [{"sopClass": "SegmentationStorage", "uid": "1.2.276.0.7230010.3.1.4.0.42154.1458337731.665796"}]}, {"uid": "1.2.392.200103.20080913.113635.1.2009.6.22.21.43.10.23430.1", "instance": [{"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23431.1"}, {"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23432.1"}, {"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23433.1"}]}]}}]}'


base_url = "http:localhost:8080/fhir_base/"


@pytest.fixture
def uploader():
    bundle_string = """
    {"resourceType": "Bundle", "entry": [{"resource": {"status": "final", "code": {"coding": [{"code": "126000", "system": "http://dicom.nema.org/resources/ontology/DCM", "display": "Imaging Measurement Report"}]}, "resourceType": "DiagnosticReport", "imagingStudy": [{"reference": "ImagingStudy/ImageLibrary"}], "performer": [{"actor": {"family": "Reader1"}}], "identifier": [{"system": "urn:dicom:uid", "value": "1.2.276.0.7230010.3.1.4.0.83735.1480019874.480726"}], "id": "DiagnosticReport", "subject": {"reference": "Patient/Patient"}}, "request": {"url": "", "method": "POST"}}, {"resource": {"resourceType": "Patient", "gender": "male", "identifier": [{"system": "urn:dicom:<<<patient_id>>>", "value": "99000"}], "id": "Patient", "name": [{"family": "JANCT000"}]}, "request": {"url": "", "method": "POST"}}, {"resource": {"resourceType": "ImagingStudy", "series": [{"instance": [{"sopClass": "SegmentationStorage", "uid": "1.2.276.0.7230010.3.1.4.0.42154.1458337731.665796"}], "uid": "1.2.276.0.7230010.3.1.3.0.42154.1458337731.665795"}, {"instance": [{"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23431.1"}, {"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23432.1"}, {"sopClass": "CTImageStorage", "uid": "1.2.392.200103.20080913.113635.2.2009.6.22.21.43.10.23433.1"}], "uid": "1.2.392.200103.20080913.113635.1.2009.6.22.21.43.10.23430.1"}], "patient": {"reference": "Patient/Patient"}, "id": "ImageLibrary", "uid": "1.2.392.200103.20080913.113635.0.2009.6.22.21.43.10.22941.1"}, "request": {"url": "", "method": "POST"}}], "type": "transaction"}
  """
    json_dict = json.loads(bundle_string)
    return BundleUploader(json_dict, base_url)


@pytest.fixture
def patched_requests_patient_existing(monkeypatch):
    # store a reference to the old get method
    old_get = requests.get
    old_post = requests.post

    def mocked_get(uri, *args, **kwargs):
        print("Performing GET request at uri %s" % uri)
        if "Patient" in uri:
            mock = type('MockedReq', (), {})()
            mock.json = lambda: json.loads(mocked_patient_available_json)
            mock.text = lambda: mocked_patient_available_json
            return mock
        else:
            return old_get(uri, args)

    def mocked_post(uri, json, *args, **kwargs):
        print("Performing POST request at uri %s" % uri)
        payload = json
        ensure_patient_resource_not_in_payload(payload)
        mock = type('MockedReq', (), {})()
        mock.json = lambda: json.loads(mocked_patient_available_return)
        mock.test = lambda: mocked_patient_available_return
        return mock
    # finally, patch Requests.get with patched version
    monkeypatch.setattr(requests, 'post', mocked_post)
    monkeypatch.setattr(requests, 'get', mocked_get)


def test_extract_patient_identifier(uploader):
    identifier = uploader.extract_patient_identifier()
    assert identifier["system"] == "urn:dicom:<<<patient_id>>>" and identifier["value"] == "99000"


def test_upload_patient_bundle_if_patient_existing(uploader, patched_requests_patient_existing):
    uploader.upload_bundle()

def ensure_patient_resource_not_in_payload(payload):
    assert len(payload["entry"]) == 2
    patient = next(entry for entry in payload["entry"] if entry["resource"]["resourceType"] == "Patient")
    assert patient == None
