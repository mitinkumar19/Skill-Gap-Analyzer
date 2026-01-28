# Implementation Plan - Predefined Roles

## Goal
Enable users to select a target job role (e.g., "Data Scientist") to automatically generate a standardized Job Description (JD) using Generative AI. This eliminates the need for manual JD copy-pasting and allows for "benchmark" comparisons.

## User Review Required
> [!IMPORTANT]
> **Latency**: Generating a high-quality JD may take a few seconds. A loading indicator is essential in the UI.

> [!NOTE]
> **Data Reuse**: Generated JDs will be stored in the Vector DB. Future iterations can query these cached definitions for speed and consistency.

## Proposed Changes

### Backend (`app/services`)
#### [MODIFY] [generator.py](file:///c:/Users/meetv/Skill gap analyzer/app/services/generator.py)
- **New Method**: `generate_job_description(role_name: str) -> str`
- **Logic**: Use the configured LLM (Groq) to generate a structured JD containing responsibilities, requirements, and tech stack for the given role.

#### [MODIFY] [app/main.py](file:///c:/Users/meetv/Skill gap analyzer/app/main.py)
- **New Endpoint**: `POST /api/v1/generate-jd`
    - Input: `{"role": "string"}`
    - Output: `{"job_description": "string"}`
- This separates generation from analysis, giving the user a chance to review/edit the generated text.

#### [MODIFY] [vector_db.py](file:///c:/Users/meetv/Skill gap analyzer/app/services/vector_db.py)
- (Optional for V1) Method to cache/retrieve JDs by role name to avoid re-generating common roles.

### Frontend (`ui/app.py`)
#### [MODIFY] [ui/app.py](file:///c:/Users/meetv/Skill gap analyzer/ui/app.py)
- **UI State**: Add a toggle/radio button: `[Paste Job Description]` vs `[Generate from Role]`.
- **New Interaction**:
    - If "Generate" is selected: Show Text Input (Role Name) + "Generate" Button.
    - On Click: Call `/api/v1/generate-jd`.
    - Result: Populate the main Job Description text area with the response.
- **Workflow**: User can then immediately click "Analyze Gap" using the generated text.

## Verification Plan

### Automated Tests
- **Unit**: Test `generator.generate_job_description` with mocked LLM response.
- **E2E**: Verify endpoint `POST /generate-jd` returns 200 and text content.

### Manual Verification
1. Launch UI.
2. Toggle to "Generate from Role".
3. Enter "Python Backend Developer".
4. Click Generate and confirm text area fills with a sensible JD.
5. Click "Analyze" and verify the report is generated correctly against the uploaded resume.
