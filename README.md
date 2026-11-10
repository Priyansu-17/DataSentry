# DataSentry

Autonomous Data Quality & Incident Response Agent - A portfolio project combining data engineering with agentic AI.

## Goal

Build an interview-ready portfolio project that demonstrates:
- Data engineering skills (Kafka, Spark, PostgreSQL, dbt, Airflow)
- Agentic AI capabilities (LangGraph, RAG, autonomous remediation)
- Production-ready engineering practices

## Project Structure

```
data/
src/
  ingestion/
  quality/
  agents/
  tools/
  api/
tests/
docker-compose.yml
```

## Quick Start

### Development with GitHub Codespaces (recommended)
1. **Fork** this repository to your own GitHub account (if you haven’t already).
2. In GitHub, click the **"Code"** button and select **"Open with Codespaces"** → **"Create new codespace"**.
3. The Codespace will automatically spin up the **devcontainer** defined in `.devcontainer/devcontainer.json`. This container runs `docker compose` for you, so PostgreSQL and the Python app are ready.
4. In the terminal that opens inside the Codespace run:
   ```bash
   docker compose up -d   # start Postgres and the app container
   python src/ingestion/generate_sample_data.py   # generate CSVs
   python src/ingestion/load_data.py              # load data into Postgres
   uvicorn src/api/app:app --host 0.0.0.0 --port 8000   # start the FastAPI server
   ```
5. VS Code will expose port 8000 – click the **"Ports"** tab, then the **"Preview"** button to open the API in your browser. You can now call endpoints like `http://localhost:8000/customers`.

### Temporary demo with Play‑With‑Docker (no GitHub account needed)
1. Open https://labs.play-with-docker.com/ and start a new session.
2. Drag‑and‑drop the repository files (or zip) into the terminal.
3. Run `docker compose up -d` and follow the same steps as above.

### Running locally (if you have Docker installed)
1. Install Docker Desktop.
2. From the project root run `docker compose up -d`.
3. Follow steps 4‑5 from the Codespaces section.

---

### Prerequisites
- Docker
- Python 3.10+
- Git

### Setup

1. Clone the repository
2. Start PostgreSQL:
   ```bash
   docker-compose up -d
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

Details to be added as components are built.

## Architecture

Full architecture will be documented as the project progresses. See `project_plan.md` for the complete roadmap.

## Documentation

- `project_plan.md` - Complete 6-week project plan
- `CHANGELOG.md` - Change history
- `PROGRESS.md` - Current progress and next steps
- `DECISIONS.md` - Architectural decisions and rationale

## License

MIT
