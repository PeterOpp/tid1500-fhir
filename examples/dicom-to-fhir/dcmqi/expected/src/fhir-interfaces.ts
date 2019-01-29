import { fhirAddress } from "./fhir-interfaces";
// Copyright (c) Fraunhofer MEVIS; Germany. All rights reserved.
// 
// -----------------------------------------------------------------------------
/*!
// \file fhir-interfaces.ts
// \author Joachim Georgii, Peter Oppermann, Joshua Holly, Demedts Daniel
// \date 08/2017
*/
// -----------------------------------------------------------------------------
export type fhirComparator = "<" | "<=" | ">=" | ">";
export type fhirSimpleQuantity = fhirQuantity;

/* tslint:disable:class-name */

export interface fhirIdentifier {
    use?: "usual" | "official" | "temp" | "secondary";
    type?: fhirCodeableConcept;
    system?: string;
    value?: string;
    period?: fhirPeriod;
    assigner?: fhirReference;
}

export interface fhirQuantity {
    value?: number;
    comparator?: fhirComparator;
    unit?: string;
    system?: string;
    code?: string | number;
}

export interface fhirRatio {
    numerator?: fhirQuantity;
    denumerator?: fhirQuantity;
}

export interface fhirHumanName {
    family?: string;
    given?: Array<string>;
    prefix?: Array<string>;
    suffix?: Array<string>;
    use?: string;
    text?: string;
}

export interface fhirCodeableConcept {
    coding?: Array<fhirCoding>;
    text?: string;
}

export interface fhirCoding {
    system?: string;
    version?: string;
    code?: string;
    display?: string;
    userSelected?: boolean;
}

export interface fhirReference {
    reference?: string;
    identifier ?: fhirIdentifier;
    display?: string;
}

export interface fhirRange {
    high?: fhirSimpleQuantity;
    low?: fhirSimpleQuantity;
}

export interface fhirPeriod {
    start?: string;
    end?: string;
}

export interface fhirFamilyMemberCondition {
    code?: fhirCodeableConcept;
    outcome?: fhirCodeableConcept;
    onsetAge?: {
     value: number;
     system?: string;
     code?: string;
    };
    onsetRange?: fhirRange;
    onsetDate?: string;
    onsetString?: string;
    note?: string;
}

export interface fhirFamilyMemberHistory extends fhirResource {
    resourceType: "FamilyMemberHistory";
    notDone?: boolean;
    notDoneReason?: fhirCodeableConcept;
    patient: fhirReference;
    date?: string;
    name?: string;
    relationship: fhirCodeableConcept;
    gender?: string;
    status: "partial" | "completed" | "entered-in-error" | "health-unknown";

    bornPeriod?: fhirPeriod;
    bornDate?: string;
    bornString?: string;

    ageAge?: number;
    ageRange?: fhirRange;
    ageString?: string;
    estimatedAge?: boolean;

    deceasedBoolean?: boolean;
    deceasedAge?: number;
    deceasedRange?: fhirRange;
    deceasedDate?: string;
    deceasedString?: string;

    condition?: Array<fhirFamilyMemberCondition>;


}

export interface fhirObservationComponent {
    code: fhirCodeableConcept;
    valueQuantity?: fhirQuantity;
    valueCodeableConcept?: fhirCodeableConcept;
    valueString?: string;
    valueRange?: fhirRange;
    valueRatio?: fhirRatio;
    valuePeriod?: fhirPeriod;
    valueAttachment?: fhirAttachment;
    dataAbsentReason?: fhirCodeableConcept;
    interpretation?: fhirCodeableConcept;
    referenceRange?: Array<fhirObservationReferenceRange>;
}

export interface fhirObservationRelated {
    type?: "has-member" | "derived-from" | "sequel-to" | "replaces" | "qualified-by" | "interfered-by";
    target: fhirReference;
}

export interface fhirObservation extends fhirResource {
    resourceType: "Observation";
    status: "registered" | "preliminary" | "final" | "amended";
    category?: Array<fhirCodeableConcept>;
    code: fhirCodeableConcept;
    subject?: fhirReference;
    context?: fhirReference;
    effectiveDateTime?: string;
    effectivePeriod?: fhirPeriod;
    performer?: Array<fhirReference>;

    valueQuantity?: fhirQuantity;
    valueCodeableConcept?: fhirCodeableConcept;
    valueString?: string;
    valueBoolean?: boolean;
    valueRange?: fhirRange;
    valueRatio?: fhirRatio;
    // valueSampledData ?: any;  //TODO
    valueAttachement ?: fhirAttachment;
    valueTime?: string;
    valueDateTime?: string;
    valuePeriod?: fhirPeriod;

    dataAbsentReason?: fhirCodeableConcept;
    interpretation?: fhirCodeableConcept;
    comment?: string;
    bodySite?: fhirCodeableConcept;
    method?: fhirCodeableConcept;
    specimen?: fhirReference;
    device?: fhirReference;
    related?: Array<fhirObservationRelated>;
    component?: Array<fhirObservationComponent>;

    referenceRange?: Array<fhirObservationReferenceRange>;
}

export interface fhirConditionStage {
    summary?: fhirCodeableConcept;
    assessment?: Array<fhirReference>;
}
export interface fhirConditionEvidence {
    code?: Array<fhirCodeableConcept>;
    detail?: Array<fhirReference>;
}

export interface fhirCondition extends fhirResource {
    resourceType: "Condition";
    clinicalStatus?: "active" | "recurrence" | "inactive" | "remission" | "resolved";
    verificationStatus?: "provisional" | "differential" | "confirmed" | "refluted" | "entered-in-error" | "unknown";
    category?: fhirCodeableConcept[];
    severity?: fhirCodeableConcept;
    code?: fhirCodeableConcept;
    bodySite?: Array<fhirCodeableConcept>;

    subject: fhirReference;
    context?: fhirReference;

    onsetDateTime?: string;
    onsetAge?: string | number;
    onsetPeriod?: fhirPeriod;
    onsetRange?: fhirRange;
    onsetString?: string;

    abatementDateTime?: string;
    abatementAge?: string | number;
    abatementBoolean?: boolean;
    abatementPeriod?: fhirPeriod;
    abatementRange?: fhirRange;
    abatementString?: string;

    assertedDate?: string;
    asserter?: fhirReference;

    stage?: fhirConditionStage;
    evidence?: Array<fhirConditionEvidence>;
}

export interface fhirDosage {
    text?: string;
    route?: fhirCodeableConcept;
    asNeededBoolean?: boolean;
    doseQuantity: fhirSimpleQuantity;
}

export interface fhirMedicationStatement extends fhirResource {
    resourceType: "MedicationStatement";
    status: "active" | "completed" | "entered-in-error" | "intended" | "stopped" | "on-hold";
    medicationCodeableConcept: fhirCodeableConcept;
    context?: fhirReference;
    category?: fhirCodeableConcept;
    effectiveDateTime?: string;
    effectivePeriod?: fhirPeriod;
    dateAsserted?: string;
    subject: fhirReference;
    dosage?: Array<fhirDosage>;
    taken: "y" | "n" | "unk" | "na";
}

export interface fhirAllergyIntolerance extends fhirResource {
    resourceType: "AllergyIntolerance";
    clinicalStatus: "active" | "inactive" | "resolved";
    verificationStatus: "unconfirmed" | "confirmed" | "refuted" | "entered-in-error";
    code: fhirCodeableConcept;
    assertedDate?: string;
    onsetDateTime?: string,
    patient: fhirReference;
    note?: string;
}

export interface fhirObservationReferenceRange {
    low?: fhirSimpleQuantity;
    high?: fhirSimpleQuantity;
    type?: fhirCodeableConcept;
    appliesTo?: Array<fhirCodeableConcept>;
    age?: fhirRange;
    text?: string;
}

export interface fhirBundle {
    resourceType: "Bundle";
    entry?: Array<fhirBundleEntry>;
    type?: string;
    total?: number;
    link?: {
        relation: string,
        url: string
    }[]
}

export interface fhirBundleEntry {
    request?: {
        method: string;
        url: string
    };
    resource: fhirResource;
    fullUrl?: string;
}

export interface fhirResource {
    id?: string;
    identifier?: fhirIdentifier[];
    resourceType: string;
    meta?: fhirMetadata;
}

export interface fhirMetadata {
    versionId?: string;
    lastUpdated?: string;
    profile?: string[];
    security?: fhirCoding[];
    tag?: fhirCoding[];
}

type fhirResourceType = fhirFamilyMemberHistory | fhirCondition | fhirObservation;

export interface fhirPerformer {
    role?: fhirCodeableConcept;
    actor: fhirReference;
}

export interface fhirImage {
    comment?: string;
    link: fhirReference;
}

export interface fhirDiagnosticReport extends fhirResource {
    resourceType: "DiagnosticReport";
    basedOn?: Array<fhirReference>;
    status: "registered" | "partial" | "preliminary" | "final";
    category?: fhirCodeableConcept;
    code: fhirCodeableConcept;
    subject?: fhirReference;
    context?: fhirReference;
    effectiveDateTime?: string;
    effectivePeriod?: fhirPeriod;
    issued?: string;
    performer?: Array<fhirPerformer>;
    specimen?: Array<fhirReference>;
    result?: Array<fhirReference>;
    imagingStudy?: Array<fhirReference>;
    image?: Array<fhirImage>;
    conclusion?: string;
    codedDiagnosis?: Array<fhirCodeableConcept>;
    presentedForm?: Array<fhirAttachment>;
}

export type fhirAvailability = "ONLINE" | "OFFLINE" | "NEARLINE" | "UNAVAILABLE";

export interface fhirImagingStudyInstance {
    uid: string;
    number?: number;
    sopClass: string;
    title?: string;
}

export interface fhirImagingStudySeries {
    uid: string;
    number?: number;
    modality: fhirCoding;
    description?: string;
    numberOfInstances?: number;
    availability?: fhirAvailability;
    endpoint?: Array<fhirReference>;
    bodySite?: fhirCoding;
    laterality?: fhirCoding;
    started?: string;
    performer?: Array<fhirReference>;
    instance?: Array<fhirImagingStudyInstance>;
}

export interface fhirImagingStudy extends fhirResource {
    resourceType: "ImagingStudy";
    uid: string;
    accession?: string;
    availability?: fhirAvailability;
    modalityList?: Array<fhirCoding>;
    patient: fhirReference;
    context?: fhirReference;
    started?: string;
    basedOn?: Array<fhirReference>;
    referrer?: fhirReference;
    interpreter?: Array<fhirReference>;
    endpoint?: Array<fhirReference>;
    numberOfSeries?: number;
    numberOfInstances?: number;
    procedureReference?: Array<fhirReference>;
    procedureCode?: Array<fhirCodeableConcept>;
    reason?: fhirCodeableConcept;
    description?: string;
    series?: Array<fhirImagingStudySeries>;
}

export interface fhirImagingManifest {
  id: string;
  resourceType: "ImagingManifest";
  identifier?: fhirIdentifier[];
  patient: fhirReference;
  authoringTime?: string;
  author?: fhirReference;
  description?: string;
  study: Array<fhirImagingManifestStudy>;
}

export interface fhirImagingManifestStudy {
  uid: string;
  imagingStudy?: fhirReference;
  endpoint?: Array<fhirReference>;
  series: Array<fhirImagingManifestSeries>;
}

export interface fhirImagingManifestSeries {
  uid: string;
  endpoint?: Array<fhirReference>;
  instance: Array<fhirImagingStudyInstance>;
}

export interface fhirImagingStudyInstance {
  uid: string;
  sopClass: string;
}

export interface fhirAttachment {
    contentType?: string;
    language?: string;
    data?: string; // base64 encoded
    url?: string;
    size?: number;
    hash?: string;
    title?: string;
    creation?: string;
}

export type fhirEpisodeOfCareStatus = "planned" | "waitlist" | "active" | "onhold" | "finished" | "cancelled" | "entered-in-error";
export interface fhirEpisodeOfCareStatusHistory {
    status: fhirEpisodeOfCareStatus;
    period: fhirPeriod;
}

export interface fhirEpisodeOfCareDiagnosis {
    condition: fhirReference;
    role?: fhirCodeableConcept;
    rank?: number;
}

export interface fhirEpisodeOfCare extends fhirResource {
    resourceType: "EpisodeOfCare";
    status: fhirEpisodeOfCareStatus;
    statusHistory?: Array<fhirEpisodeOfCareStatusHistory>;
    type?: Array<fhirCodeableConcept>;
    diagnosis?: Array<fhirEpisodeOfCareDiagnosis>;
    patient: fhirReference;
    managingOrganization?: fhirReference;
    period?: fhirPeriod;
    referralRequest?: Array<fhirReference>;
    careManager?: fhirReference;
    team?: Array<fhirReference>;
    account?: Array<fhirReference>;
}

export interface fhirProcedureRequest extends fhirResource {
    resourceType: "ProcedureRequest";
    definition?: Array<fhirReference>;
    basedOn?: Array<fhirReference>;
    replaces?: Array<fhirReference>;
    status: "draft" | "active" | "suspended" | "completed" | "entered-in-error" | "cancelled";
    intent: "proposal" | "plan" | "ordered";
    priority?: "routine" | "urgent" | "asap" | "stat";
    doNotPerform?: boolean;
    category?: Array<fhirCodeableConcept>;
    code: fhirCodeableConcept;
    subject: fhirReference;
    context?: fhirReference;
    occurenceDateTime?: string;
    occurencePeriod?: fhirPeriod;
    occurenceTiming?: any;
    asNeededBoolean?: boolean;
    asNeededCodeableConcept?: fhirCodeableConcept;
    authoredOn?: string;
    requester?: {
        agent: fhirReference;
        onBehalfOf?: fhirReference
    };
    performerType?: fhirCodeableConcept;
    performer?: fhirReference;
    reasonCode?: Array<fhirReference>;
    reasonReference?: Array<fhirReference>;
    supportingInfo?: Array<fhirReference>;
    speciment?: Array<fhirReference>;
    bodySite?: Array<fhirCodeableConcept>;
    note?: Array<fhirAnnotation>;
    relevantHistory?: Array<fhirReference>;
}

export interface fhirProcedurePerformer {
    role?: fhirCodeableConcept;
    actor: fhirReference;
    onBehalfOf?: fhirReference;
}

export type fhirProcedureStatus =  "preparation" | "in-progress" | "suspended" | "aborted" | "completed" | "entered-in-error" | "unknown";

export interface fhirProcedure extends fhirResource {
    resourceType: "Procedure";
    definition?: Array<fhirReference>;
    basedOn?: Array<fhirReference>;
    partOf?: Array<fhirReference>;
    status: fhirProcedureStatus;
    notDone?: boolean;
    notDoneReason?: fhirCodeableConcept;
    category?: fhirCodeableConcept;
    code?: fhirCodeableConcept;
    subject: fhirReference;
    context?: fhirReference;
    performedDateTime?: string;
    performedPeriod?: fhirPeriod;
    performer?: Array<fhirProcedurePerformer>;
    location?: fhirReference;
    reasonCode?: Array<fhirCodeableConcept>;
    reasonReference?: Array<fhirReference>;
    bodySite?: Array<fhirCodeableConcept>;
    outcome?: fhirCodeableConcept;
    report?: Array<fhirReference>;
    complication?: Array<fhirCodeableConcept>;
    followUp?: Array<fhirCodeableConcept>;
    note?: Array<fhirAnnotation>;
    focalDevice?: Array<any>;
    usedReference?: Array<fhirReference>;
    usedCode?: Array<fhirCodeableConcept>;
}

export interface fhirAddress {
    use?: "home" | "work" | "temp" | "old";
    text?: string;
    // other fields nod added; because not needed
}

export interface fhirPatientLink {
    other: fhirReference;
    type: "replaced-by" | "replaces" | "refer" | "seealso";
}

export interface fhirPatient extends fhirResource {
    identifier?: Array<fhirIdentifier>;
    resourceType: "Patient";
    active?: boolean;
    name?: Array<fhirHumanName>;
    telecom?: any;
    gender?: "male" | "female" | "other" | "unknown";
    birthDate?: string;
    deceasedBoolean?: boolean;
    deceasedDateTime?: string;
    address?: Array<fhirAddress>;
    martialStatus?: fhirCodeableConcept;
    multipleBirthBoolean?: boolean;
    multipleBirthInteger?: number;
    photo?: Array<fhirAttachment>;
    contact?: any;
    animal?: any;
    communication?: any;
    generalPractitioner?: Array<any>;
    link?: Array<fhirPatientLink>;
}

export type fhirEncounterStatus = "planned" | "arrived" | "triaged" | "in-progress" | "onleave" | "finished" | "cancelled";

export interface fhirEncounterStatusHistory {
    status: fhirEncounterStatus;
    period: fhirPeriod;
}

export interface fhirEncounterDiagnosis {
    condition: fhirReference;
    role?: fhirCodeableConcept;
    rank?: number;
}

export interface fhirEncounter extends fhirResource {
    resourceType: "Encounter";
    status: fhirEncounterStatus;
    statusHistory?: Array<fhirEncounterStatusHistory>;
    class?: "inpatient" | "outpatient" | "ambulatory" | "emergency";
    type?: Array<fhirCodeableConcept>;
    priority?: fhirCodeableConcept;
    subject: fhirReference;
    episodeOfCare?: Array<fhirReference>;
    incomingReferral?: Array<fhirReference>;
    participant?: Array<any>;
    period?: fhirPeriod;
    length?: fhirQuantity;
    reason?: Array<fhirCodeableConcept>;
    diagnosis?: Array<fhirEncounterDiagnosis>;
    // others in the standard; though not used here
}

export interface fhirCarePlan extends fhirResource {
  id: string;
  resourceType: "CarePlan";
  identifier?: fhirIdentifier[];
  basedOn?: fhirReference[];
  replaces?: fhirReference[];
  partOf?: fhirReference[];

  status: "draft" | "active" | "suspended" | "completed" | "entered-in-error" | "cancelled" | "unknown";
  intent: "proposal" | "plan" | "order" | "option";
  category?: fhirCodeableConcept[];
  title?: string;
  description?: string;
  subject: fhirReference;
  context?: fhirReference;
  period?: fhirPeriod;
  author?: fhirReference[];
  careTeam?: fhirReference[];
  addresses?: fhirReference[];
  supportingInfo?: fhirReference[];
  goal?: fhirReference[];

  activity?: fhirCarePlanActivity[];
  note?: fhirAnnotation[];
}

export interface fhirCarePlanActivity {
  outcomeCodeableConcept?: fhirCodeableConcept[];
  outcomeReference?: fhirReference[];
  progress?: fhirAnnotation[];
  reference?: fhirReference[];

  detail?: fhirCarePlanActivityDetail;
}

export interface fhirCarePlanActivityDetail {
  category?: fhirCodeableConcept;
  definition?: fhirReference;
  code?: fhirCodeableConcept;
  reasonCode?: fhirCodeableConcept[];
  reasonReference?: fhirReference[];
  goal?: fhirReference[];

  status: "not-started" | "scheduled" | "in-progress" | "on-hold" | "completed" | "cancelled" | "unknown";
  statusReason?: string;
  prohibited?: boolean;

  scheduleTiming?: any; // TODO: add fhirTiming
  schedulePeriod?: fhirPeriod;
  scheduleString?: string;

  location?: fhirReference;
  performer?: fhirReference[];

  productCodeableConcept?: fhirCodeableConcept;
  productReference?: fhirReference;

  dailyAmount?: fhirSimpleQuantity;
  quantity?: fhirSimpleQuantity;
  description?: string;
}


export interface fhirMedia extends fhirResource {
    resourceType: "Media";
    type: "photo" | "video" | "audio";
    subtype?: fhirCodeableConcept;
    view?: fhirCodeableConcept;
    subject?: fhirReference;
    context?: fhirReference;
    occurenceDateTime?: string;
    occurencePeriod?: fhirPeriod;
    operator?: fhirReference;
    reasonCode?: Array<fhirCodeableConcept>;
    bodySite?: fhirCodeableConcept;
    device?: fhirReference;
    height?: number;
    width?: number;
    frames?: number;
    duration?: number;
    content: fhirAttachment;
    note?: Array<fhirAnnotation>;
}

export interface fhirAnnotation {
  author?: {
    authorString?: string;
    authorReference?: fhirReference
  };
  time?: string;
  text: string;
}

export interface fhirActor {
  role: fhirCodeableConcept;
  referece: fhirReference;
}

export interface fhirConsentExcept {
  type: "deny" | "permit";
  period?: fhirPeriod;
  actor?: fhirActor[];
  action?: fhirCodeableConcept[];
  purpose?: fhirCoding[];
  class?: fhirCoding[];
  code?: fhirCoding[];
  dataPeriod?: fhirPeriod;
}

export interface fhirConsent {
  id: string;
  resourceType: "Consent";
  identifier?: fhirIdentifier[];
  status: string;
  category?: fhirCodeableConcept[];
  patient: fhirReference;
  period?: fhirPeriod;
  dateTime?: string;
  consentingParty?: fhirReference[];
  actor?: fhirActor[];
  action?: fhirCodeableConcept[];
  organization?: fhirReference[];
  sourceAttachment?: fhirAttachment;
  sourceIdentifier?: fhirIdentifier;
  sourceReference?: fhirReference;
  // ...
  purpose?: fhirCoding[];
  dataPeriod?: fhirPeriod;
  except?: fhirConsentExcept[];
}

export interface fhirPractitionerQualification {
  identifier?: fhirIdentifier[],
  code: fhirCodeableConcept,
  period?: fhirPeriod,
  issuer?: fhirReference
}

export interface fhirPractitioner {
  id: string;
  resourceType: "Practitioner";
  identifier?: Array<fhirIdentifier>;
  active?: boolean;
  name?: fhirHumanName[];
  telecom?: any;
  address?: fhirAddress[];
  gender?: "male" | "female" | "other" | "unknown";
  birthDate?: string;
  photo?: Array<fhirAttachment>;
  qualification?: fhirPractitionerQualification[];
  communication?: fhirCodeableConcept[];
}
