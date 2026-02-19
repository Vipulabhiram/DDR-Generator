import streamlit as st
import requests

st.set_page_config(page_title="UrbanRoof DDR Generator", layout="wide")

st.title("🏢 Detailed Diagnostic Report Generator")
st.markdown(
    "Upload Inspection and Thermal reports (.pdf or .txt) to generate a structured client-ready DDR."
)

st.divider()


col1, col2 = st.columns(2)

with col1:
    inspection_file = st.file_uploader(
        "Upload Inspection Report",
        type=["pdf", "txt"]
    )

with col2:
    thermal_file = st.file_uploader(
        "Upload Thermal Report",
        type=["pdf", "txt"]
    )

st.divider()

if st.button("Generate DDR"):

    if not inspection_file or not thermal_file:
        st.error("Please upload both inspection and thermal reports.")
    else:
        with st.spinner("Analyzing reports and generating DDR..."):

            response = requests.post(
                "http://127.0.0.1:8000/generate-ddr",
                files={
                    "inspection_file": (
                        inspection_file.name,
                        inspection_file.getvalue(),
                        inspection_file.type
                    ),
                    "thermal_file": (
                        thermal_file.name,
                        thermal_file.getvalue(),
                        thermal_file.type
                    )
                }
            )

            if response.status_code == 200:
                ddr = response.json()

                st.success("DDR Generated Successfully")
                st.divider()


                st.header("📋 Property Issue Summary")
                st.write(ddr.get("property_issue_summary", "Not Available"))

                st.divider()

                st.header("📍 Area-wise Observations")
                for obs in ddr.get("area_wise_observations", []):
                    with st.container():
                        st.subheader(f"Area: {obs.get('area', 'Not Available')}")
                        st.write(f"**Observation:** {obs.get('observation', 'Not Available')}")
                        st.write(f"**Thermal Evidence:** {obs.get('thermal_evidence', 'Not Available')}")
                        st.divider()

                st.header("🧠 Probable Root Cause")
                st.write(ddr.get("probable_root_cause", "Not Available"))

                st.divider()

                st.header("⚠ Severity Assessment")
                severity = ddr.get("severity_assessment", {})
                st.write(f"**Level:** {severity.get('level', 'Not Available')}")
                st.write(f"**Reasoning:** {severity.get('reasoning', 'Not Available')}")

                st.divider()

                st.header("🛠 Recommended Actions")
                for action in ddr.get("recommended_actions", []):
                    st.write(f"- {action}")

                st.divider()

                st.header("📝 Additional Notes")
                st.write(ddr.get("additional_notes", "Not Available"))

                st.divider()

                st.header("❓ Missing / Unclear Information")
                for item in ddr.get("missing_information", []):
                    st.write(f"- {item}")

               

            else:
                st.error("Error generating DDR. Please check backend logs.")
