# Mental Health Agent System — Capstone Project

## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Architecture](#architecture)
- [Data Flow & Components](#data-flow--components)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Diagrams & Images](#diagrams--images)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Problem Statement
Many users seeking mental health support face barriers: limited access to professionals, long wait times, and stigma. The goal of this capstone project is to build a prototype **Mental Health Agent System** that can:
- Provide an initial conversational intake and triage.
- Offer evidence-based coping strategies and resources.
- Detect high-risk phrases and escalate appropriately (e.g., suggest emergency help).
- Log anonymized interactions for model improvement and analysis.

This README explains the problem, the proposed solution, the architecture, setup instructions, and includes diagrams to help onboarding.

---

## Solution Overview
The system is designed as a modular conversational agent (chatbot) with the following capabilities:
1. **User Interaction Layer** — accepts user text input (web UI or CLI/notebook).
2. **NLP & Intent Processing** — preprocesses text, classifies intent (triage, well-being check, crisis), and extracts entities.
3. **Response Generation** — uses templates and rule-based responses for deterministic content, and an optional ML-backed generator for more natural replies.
4. **Safety & Escalation** — monitors for high-risk content and presents escalation options with local emergency resources.
5. **Logging & Analytics** — anonymized logs are stored with minimal PII, and basic analytics are computed for research.

Key design principles:
- **Privacy-first**: avoid storing personally identifying information, encrypt logs if retained.
- **Explainability**: deterministic rules for safety-critical decisions.
- **Modularity**: independent components to allow swapping ML models or interface.

---

## Architecture
High-level components are shown in `architecture_diagram.png`.

**Components**
- **Frontend (Notebook / Web UI)**: User-facing input/output.
- **API / Controller**: Routes messages to processors and returns responses.
- **NLP Module**: Tokenization, intent classification, entity recognition.
- **Safety Module**: Rule engine for crisis detection (keywords, sentiment thresholds), escalation flows.
- **Response Engine**: Templates + optional generative model.
- **Database / Logger**: Stores anonymized interactions and metadata.

Refer to the `Diagrams & Images` section below for the PNG files included in this package.

---

## Data Flow & Components
See `data_flow.png` for a simplified flowchart.

Step-by-step:
1. User sends message via frontend.
2. Controller forwards the message to the NLP Module.
3. NLP Module outputs intent + entities + sentiment.
4. Safety Module checks outputs for crisis indicators.
   - If crisis detected → escalate: show emergency resources and (optionally) notify human reviewer.
   - Else → Response Engine prepares a reply (template-based or generator).
5. Reply is returned to frontend and the interaction is logged (anonymized) in the Logger.

Notes on anonymization:
- Strip names, emails, phone numbers before logging.
- Keep only message-level metadata (timestamp, intent label, anonymized id).
- Rotate logs frequently and restrict access.

---

## Setup & Installation

### Requirements
- Python 3.10+ recommended
- A virtual environment tool (venv or conda)
- Basic packages (example):
  - numpy
  - pandas
  - scikit-learn (for simple classifiers)
  - nltk or spacy (for NLP)
  - flask or fastapi (if exposing an HTTP API)
  - jupyter (if using the notebook)

### Quick Setup (local)
```bash
# 1. clone the repo or unzip the package
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.\.venv\Scripts\activate      # Windows PowerShell

pip install --upgrade pip
pip install numpy pandas scikit-learn nltk spacy flask jupyter
# (Adjust to your preferred library choices)
```

### Optional: Install spaCy English model
```bash
python -m spacy download en_core_web_sm
```

---

## Running the Project

### Running the Notebook
1. Ensure your virtual environment is active and dependencies are installed.
2. Start Jupyter:
```bash
jupyter notebook
```
3. Open `mental-health-agent-system-capstone-project (5).ipynb` (included in this zip) and run cells in order. The notebook contains exploratory code, data preprocessing, and demo interaction cells.

### Running as a Minimal API (example)
If you wrap the controller into a Flask app:
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```
Then point a simple frontend or use `curl` to POST messages to the `/message` endpoint.

---

## Example Usage
A short pseudo-example of a conversation flow inside the notebook:
1. User: "I've been feeling really anxious lately and can't sleep."
2. Agent: (NLP) intent=`anxiety_check`, sentiment=`negative`
3. Safety Module: no crisis keywords -> Response Engine returns grounding techniques + breathing exercise and links to resources.
4. Log saved (anonymized).

---

## Project Structure
```
/ (root)
├─ README.md
├─ architecture_diagram.png
├─ data_flow.png
├─ mental-health-agent-system-capstone-project (5).ipynb
├─ /models
│   └─ intent_classifier.pkl
├─ /notebooks
│   └─ experiments.ipynb
├─ /src
│   ├─ nlp.py
│   ├─ safety.py
│   └─ response_engine.py
└─ requirements.txt
```

Adjust names to match your repository.

---

## Diagrams & Images
This package includes:
- `architecture_diagram.png` — high-level architecture overview.
- `data_flow.png` — step-by-step data flow.

These diagrams are simplistic and meant for documentation. Replace them with formal diagrams (drawn in Figma, draw.io, or diagrams.net) if desired.

---

## Contributing
If you'd like to extend the system:
1. Fork the repository.
2. Create a feature branch `feature/your-feature`.
3. Submit PR with tests and documentation updates.
4. For safety-critical changes (safety module, escalation rules) please include a short rationale and test cases.

---

## License
Choose an appropriate license for your project (MIT, Apache-2.0, etc). Example: MIT License.

---

## Contact
Project author / maintainer: *Anwesha Debnath*  — update to your preferred contact information.

---