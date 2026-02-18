# Detailed Diagnostic Report Generator

## Overview

This project builds an AI workflow that converts technical inspection and thermal reports into a structured, client-ready Detailed Diagnostic Report (DDR).

The system reads raw site documents and generates a professional report in a clear and organized format.

It demonstrates:

- AI reasoning
- Structured data extraction
- Logical merging of multiple documents
- Handling imperfect or missing inputs
- Schema validation using Pydantic
- Clean backend + frontend architecture

---

## Problem Statement

Given:

- Inspection Report (site observations)
- Thermal Report (temperature findings)

The system must:

- Extract relevant observations
- Combine both documents logically
- Avoid duplicate points
- Detect missing or conflicting information
- Generate a structured client-friendly DDR
- Avoid inventing facts

---

## DDR Output Structure

The generated report includes:

1. Property Issue Summary  
2. Area-wise Observations  
3. Probable Root Cause  
4. Severity Assessment (with reasoning)  
5. Recommended Actions  
6. Additional Notes  
7. Missing or Unclear Information  

If information is missing, the system explicitly mentions **"Not Available"**.

---

## Tech Stack

- Python
- FastAPI (Backend API)
- Streamlit (Minimal UI)
- Groq LLM API
- Pydantic (Schema validation)

---

## How It Works

1. User uploads Inspection and Thermal reports.
2. Backend extracts structured observations using LLM prompts.
3. Extracted findings are merged and cleaned.
4. Final DDR is generated in structured JSON format.
5. Streamlit displays the formatted report.

The workflow ensures reliability and prevents hallucinated data.

# How to run this
-Create a VE
-Install all required dependeceys(requirements.txt)
-create .env file and past your groq API key with key name as GROQ_API_KEY 
-you should run both backend and frontend separetly 
-run uvicorn app.main:app --reload for  backend(To start a server)
-run streamlit run streamlit_app.py for frontend 
