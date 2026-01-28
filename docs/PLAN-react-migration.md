# Plan: Migrate Frontend to React

> **Status**: PROPOSED
> **Goal**: Replace existing Streamlit frontend with a modern, high-performance React application using the "Clean SaaS" aesthetic.

## User Review Required
> [!IMPORTANT]
> **Architecture Change**: The functionality is moving from a monolithic-style script (`ui/app.py`) to a decoupled Client-Server architecture.
> - **Frontend**: React + Vite (Port 5173)
> - **Backend**: FastAPI (Port 8000)
>
> You will need to run two separate terminals to start the full application.

## Proposed Changes

### 1. Backend Configuration `app/`
We need to enable the React frontend to communicate with the FastAPI backend.

#### [MODIFY] [main.py](file:///c:/Users/meetv/Skill%20gap%20analyzer/app/main.py)
- **Add CORS Middleware**: Allow `http://localhost:5173` to make requests.
- **Verify Endpoints**: Ensure `/api/v1/analyze` and `/api/v1/generate-skills` handle JSON/Form data consistently for the new frontend.

### 2. Frontend Initialization `client/` (New)
Create a clean slate React project.

#### [NEW] Project Structure
- **Technical Stack**:
    - Vite (Build Tool)
    - React 19 (UI Library)
    - TypeScript (Type Safety)
    - TailwindCSS (Styling)
    - Shadcn/UI (Component Library)
    - Lucide React (Icons)
    - Recharts or Plotly.js (Charts - replacing Python Plotly)
    - Axios/Tanstack Query (API Fetching)

#### [NEW] Key Components
- **Layout**: `Navbar`, `Footer`, `MainLayout` (SaaS style, clean white/gray palette).
- **Features**:
    - `ResumeUploader`: Drag & drop zone for PDF.
    - `JobDescriptionInput`: Tabs for "Paste Text" vs "Generate from Role".
    - `SkillsEditor`: Interactive tag/list editor for required skills.
    - `AnalysisDashboard`:
        - `MatchScore`: Gauge/Progress circle.
        - `SkillGapList`: Visual comparison of matched/missing skills.
        - `LearningRoadmap`: Markdown renderer for the AI study plan.

### 3. Documentation
#### [MODIFY] [README.md](file:///c:/Users/meetv/Skill%20gap%20analyzer/README.md)
- Add "Getting Started" guide for the new Frontend.
- Update run commands (e.g., `npm run dev` + `uvicorn app.main:app`).

## Verification Plan

### Automated Tests
- **Frontend**: Check build passes (`npm run build`).
- **Linting**: Ensure no ESLint errors.

### Manual Verification
1.  **Environment Setup**: Start Backend (8000) and Frontend (5173).
2.  **Flow Test**:
    - Upload a PDF resume.
    - Enter a Job Role (e.g., "Frontend Engineer").
    - Generate Skills list -> Verify API call to `/generate-skills`.
    - Edit Skills -> Verify state update.
    - Click "Analyze" -> Verify API call to `/analyze`.
    - **Result**: Verify Score, Missing Skills, and Roadmap display correctly.
3.  **UI Check**: Ensure "Clean SaaS" aesthetic (typography, spacing, colors) is applied.
