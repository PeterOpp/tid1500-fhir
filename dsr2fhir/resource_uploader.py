import asyncio
import requests
import json

class BundleUploader:

    def __init__(self, fhir_bundle, server_base_url):
        self.fhir_bundle = fhir_bundle
        self.server_base_url = server_base_url

    '''
  Uploads the bundle in a specific order and checks for existing resources
  in every step.

  1st: Try to find if a patient with the Identifier of the DicomPatientId 
    is present already, if yes, fetch it and change all patient references
    to this one. Reove the patient resource from the fhir_bundle

  2nd: Try to fetch the diagnostic report with the same Identifier (SOPInstanceUid of
    the Dicom SR). If successfull, the report is already uploaded and we need not 
    do anything, if not, procede

  '''

    def upload_bundle(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.upload_async())

    async def upload_async(self):
        identifier = self.extract_patient_identifier()
        response = await self.request_patient_file_with_identifier(identifier)
        if len(response["entry"]) > 0:
            id = response["entry"][0]["resource"]["id"]
            self.replace_patient_id_in_bundle(id)
        
        response = await self.perform_post_to_server()
        print(response.text)

    def extract_patient_identifier(self):
        patients = self.get_resources_of_type("Patient")
        assert len(patients) == 1
        patient = patients[0]
        assert "identifier" in patient and len(patient) > 0
        identifier = self.get_identifier_with_system(
            patient["identifier"], "urn:dicom:<<<patient_id>>>")
        return identifier

    def get_resources_of_type(self, type):
        return [entry["resource"] for entry in self.fhir_bundle["entry"] if entry["resource"]["resourceType"] == type]

    def get_identifier_with_system(self, identifier_list, system):
        valid_identifiers = [
            id for id in identifier_list if id["system"] == system]
        if len(valid_identifiers) > 0:
            return valid_identifiers[0]
        else:
            return None

    async def request_patient_file_with_identifier(self, identifier):
        url = self.request_url_with_type_and_identifier("Patient", identifier)
        loop = asyncio.get_event_loop()
        response =  await loop.run_in_executor(None, requests.get, url)
        return response.json()

    def request_url_with_type_and_identifier(self, res_type, identifier):
        return "%s/%s?identifier=%s|%s" % (self.server_base_url, res_type, identifier["system"], identifier["value"])

    def replace_patient_id_in_bundle(self, new_patient_id):
        reference = dict(
            reference = "Patient/" + new_patient_id
        )
        for diagnostic_report in self.get_resources_of_type("DiagnosticReport"):
            diagnostic_report["subject"] = reference
        for imaging_study in self.get_resources_of_type("ImagingStudy"):
            imaging_study["patient"] = reference
        for observation in self.get_resources_of_type("Observation"):
            observation["subject"] = reference
        entries_without_patient = [ e for e in self.fhir_bundle["entry"] if not e["resource"]["resourceType"] == "Patient"]
        self.fhir_bundle["entry"] = entries_without_patient


    async def perform_post_to_server(self):
        url = "%s/" % self.server_base_url
        return requests.post(url, json = self.fhir_bundle)
        #return await loop.run_in_executor(None, requests.post, url,)