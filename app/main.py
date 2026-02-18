from fastapi import FastAPI, UploadFile, File
from app.schemas import DDRReport
from app.llm_service import call_llm
from app.prompts import EXTRACTION_SYSTEM_PROMPT, DDR_SYSTEM_PROMPT

import pdfplumber
import io
import json
import re

app = FastAPI()


def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


@app.post("/generate-ddr", response_model=DDRReport)
async def generate_ddr(
    inspection_file: UploadFile = File(...),
    thermal_file: UploadFile = File(...)
):

    inspection_bytes = await inspection_file.read()
    thermal_bytes = await thermal_file.read()

    # Extract text depending on file type
    if inspection_file.content_type == "application/pdf":
        inspection_text = extract_text_from_pdf(inspection_bytes)
    else:
        inspection_text = inspection_bytes.decode("utf-8")

    if thermal_file.content_type == "application/pdf":
        thermal_text = extract_text_from_pdf(thermal_bytes)
    else:
        thermal_text = thermal_bytes.decode("utf-8")

    
    inspection_prompt = f"""
    Extract key observations from this inspection report:

    {inspection_text}
    """

    inspection_extracted = call_llm(
        EXTRACTION_SYSTEM_PROMPT,
        inspection_prompt
    )

    thermal_prompt = f"""
    Extract key findings from this thermal report:

    {thermal_text}
    """

    thermal_extracted = call_llm(
        EXTRACTION_SYSTEM_PROMPT,
        thermal_prompt
    )

    
    ddr_prompt = f"""
    Using the inspection findings below:

    {inspection_extracted}

    And the thermal findings below:

    {thermal_extracted}

    Generate a Detailed Diagnostic Report strictly matching the required schema.
    Avoid duplicates.
    Mention conflicts if any.
    Return only raw JSON.
    """

    final_ddr = call_llm(
        DDR_SYSTEM_PROMPT,
        ddr_prompt
    )

    try:
        cleaned_output = re.sub(r"```json|```", "", final_ddr).strip()
        return json.loads(cleaned_output)
    except Exception as e:
        return {
            "property_issue_summary": final_ddr,
            "area_wise_observations": [],
            "probable_root_cause": "Not Available",
            "severity_assessment": {
                "level": "Not Available",
                "reasoning": f"JSON parsing failed: {str(e)}"
            },
            "recommended_actions": [],
            "additional_notes": "Not Available",
            "missing_information": ["Structured output parsing failed"]
        }
