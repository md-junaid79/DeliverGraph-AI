# DeliverGraph AI — Real-time Delivery Pricing Engine powered by LangGraph  🚚🤖

> 📦 A workflow-driven delivery cost calculator that uses LangGraph nodes to compute prices dynamically based on distance, material type, urgency, weight, and location.

---

## ⚡ Clone & environment setup (quick)

Follow these steps to get a dev copy running (Windows / PowerShell commands):

1. Clone the repository:

```powershell
git clone https://github.com/md-junaid79/DeliverGraph-AI.git
cd DeliverGraph-AI
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file in the project root for sensitive configuration (example):

```
# .env (example)
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@example.com
# Optional if you wire LLMs later
OPENAI_API_KEY=your_openai_api_key_here
```

Notes:
- If you don't provide `SENDGRID_API_KEY`, email sending will be skipped or handled by the fallback logic (saved locally).
- For testing without a `.env` file, you can set environment variables in PowerShell:

```powershell
$env:SENDGRID_API_KEY = "your_key_here"
$env:SENDGRID_FROM_EMAIL = "noreply@example.com"
```
5. Run the  app (development):

```powershell
python python -m src.api.main
```

## ▶️ Quick run (dev)

1. Install deps and start the app (FastAPI server contains the workflow runner in `src/api/main.py`):

```powershell
pip install -r requirements.txt
python -m src.api.main
```

2. Alternatively, you can import the compiled `app` from `src.workflow` in a Python REPL and call it with a sample payload for faster iteration.

---



## 🚀 Project purpose (GenAI + Workflow)

- Provide a reproducible, explainable pricing workflow using LangGraph (state graph) primitives.
- Use small deterministic GenAI-style components (templated messages, explanations, validation rules) to produce human-readable action logs and notifications.
- Keep the system testable and inspectable: every node appends to an `action_log` so you can audit decisions.

---

## 🧭 Core LangGraph components

The compiled workflow lives in `src/workflow.py`. Key node functions are in `src/nodes/`.

Nodes (files) and responsibilities:

- `src/nodes/input_node.py` — input validation, ticket generation, initial state creation ✅
- `src/nodes/distance_node.py` — distance normalization and base price estimation 📏
- `src/nodes/material_node.py` — material-type pricing adjustments (fragile, perishable, heavy) 📦
- `src/nodes/urgency_node.py` — urgency multiplier selection ⏱️
- `src/nodes/weight_node.py` — weight surcharge / volume handling ⚖️
- `src/nodes/location_node.py` — location-based adjustments (urban/rural/remote) 🗺️
- `src/nodes/final_price_node.py` — compute final price, create breakdown and totals 💰
- `src/nodes/notification_node.py` — format user-facing notification (email or UI message) ✉️
- `src/nodes/error_handler.py` — centralized error state handling and logging 🚨

These nodes are wired in `src/workflow.py` with error-branching that routes to `error_handler` when `state['error_message']` appears.

---

## 🔁 Workflow flow (step-by-step)

High-level flow (as implemented in `src/workflow.py`):

1. Input Node — validate incoming payload, create `ticket_id`, initialize `action_log = []` 🔹
2. Distance Node — verify/normalize `distance`, estimate `base_price` based on distance 🔹
3. Material Node — apply material multipliers or surcharges (fragile/perishable/heavy) 🔹
4. Urgency Node — determine urgency multiplier (normal/express/overnight) 🔹
5. Weight Node — add per-kg/volume surcharge if thresholds crossed 🔹
6. Location Node — remote area adjustments, zone pricing 🔹
7. Final Price Node — aggregate breakdown, compute `total_price`, append final actions to `action_log` ✅
8. Notification Node — generate the user message (templated HTML/email content) and optionally trigger email via `src/api/notifications.py` ✉️
9. END — workflow finishes; result includes `ticket_id`, `total_price`, `breakdown`, and `action_log` 📦

Error path: any node may set `state['error_message']` and the workflow will route to `error_handler` which records the error and terminates the flow with an error result.

---

## 🗂️ Outputs & images

- Generated artifacts (action traces, screenshots, example images) are stored under the `static/images/` and `outputs/` folders when produced. Add example images to `outputs/images/` for demo purposes.

- Recommended layout:
  - `outputs/images/` — generated visuals (e.g., pricing breakdown charts, map snapshots)
  - `outputs/traces/` — JSON traces or workflow run logs

- Example links (relative):
  - ./static/images/ — (UI images & icons used by the frontend)
  - ./outputs/images/ — (place to store generated outputs for demos)

If you run the workflow and want to save visual artifacts, write them into `outputs/images/` and link them from the templates or README for easy demoing.

---

## 🧪 GenAI aspects and determinism

- The project uses templated, deterministic GenAI-style components (no heavy LLM calls by default). Nodes emit human-readable explanations and decision traces into `action_log`.
- This makes the pipeline auditable and easy to unit-test. If you later wire LLMs, wrap them and record both prompt and model response into `action_log` for traceability.

---

## 🛠️ Where to look in code (quick links)

- Workflow entry & compile: `./src/workflow.py` ↦ creates the compiled LangGraph workflow
- Node implementations: `./src/nodes/*.py` ↦ each node is a small, testable function
- State helper utilities: `./src/utils/` ↦ helpers used by nodes
- Persistence: `./src/database/` ↦ SQLAlchemy models and CRUD helpers
- Notifications: `./src/api/notifications.py` ↦ email formatting / sending (optional)

---


## Author

Md Junaid

- GitHub: https://github.com/md-junaid79
- Project: 📦DeliverGraph-🤖AI


## ❤️ Contributing & experiments

- Add small node functions that accept and return state dicts — keep them pure and append human-readable lines to `action_log`.
- Add unit tests for node logic under `tests/` or `src/tests/`.
- If you want, I can add a small demo script that runs a sample payload through the compiled workflow and writes a trace + demo images to `outputs/`.

---

