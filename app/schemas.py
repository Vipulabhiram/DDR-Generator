from pydantic import BaseModel
from typing import List, Optional


class AreaObservation(BaseModel):
    area: str
    observation: str
    thermal_evidence: Optional[str] = "Not Available"


class SeverityAssessment(BaseModel):
    level: str
    reasoning: str


class DDRReport(BaseModel):
    property_issue_summary: str
    area_wise_observations: List[AreaObservation]
    probable_root_cause: str
    severity_assessment: SeverityAssessment
    recommended_actions: List[str]
    additional_notes: Optional[str] = "Not Available"
    missing_information: List[str]


class ReportInput(BaseModel):
    inspection_report: str
    thermal_report: str
