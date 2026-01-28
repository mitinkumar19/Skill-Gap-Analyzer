# Implementation Plan - Interactive Skill Editor

## Goal
Replace the "Text Generation -> Paste" workflow with a "Structured Skill List -> Edit -> Analyze" workflow. Users will see a list of key skills for a role, can add/remove them, and then run the gap analysis against this precise list.

## Proposed Changes

### Backend (`app/services`)
#### [MODIFY] [generator.py](file:///c:/Users/meetv/Skill gap analyzer/app/services/generator.py)
- **New Method**: `generate_skills_list(role: str) -> List[str]`
- **Logic**: Prompt LLM to return strictly a JSON list of technical and soft skills.
- **Refactor**: Remove or deprecate `generate_job_description`.

#### [MODIFY] [app/main.py](file:///c:/Users/meetv/Skill gap analyzer/app/main.py)
- **New Endpoint**: `POST /api/v1/generate-skills`
    - Input: `{"role": "string"}`
    - Output: `{"skills": ["Python", "SQL", ...]}`
- **Update Endpoint**: `POST /api/v1/analyze`
    - Update input model to accept `skills_list: List[str]` instead of (or in addition to) `job_description` text.

#### [MODIFY] [analyzer.py](file:///c:/Users/meetv/Skill gap analyzer/app/services/analyzer.py)
- **Refactor**: Update `analyze` method to handle a direct list of skills.
- **Optimization**: If a list is provided, skip the "Chunk Extraction" step and go straight to Embedding -> Matching.

### Frontend (`ui/app.py`)
#### [MODIFY] [ui/app.py](file:///c:/Users/meetv/Skill gap analyzer/ui/app.py)
- **New UI Flow**:
    1. Enter Role -> Click "Generate Skills".
    2. Display `st.data_editor` (editable table) or `st.text_area` (one per line) with the generated list.
    3. User edits list (adds/removes skills).
    4. Click "Analyze Gap".
- **Payload**: Send the final list of skills to the backend.

## Verification Plan

### Automated Tests
- **Unit**: Verify `generate_skills_list` returns a valid list.
- **Unit**: Verify `analyze` works correctly with `skills_list` input.

### Manual Verification
1. Enter "Data Engineer".
2. Verify list includes expected skills (Spark, SQL, Python).
3. Add a fake skill "Underwater Basket Weaving".
4. Analyze and check if the fake skill appears in "Missing Skills".
