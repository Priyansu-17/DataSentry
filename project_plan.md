# Project Plan: Autonomous Data Quality & Incident Response Agent

**Goal:** Data Engineering + Agentic AI interview-ready portfolio project
**Approach:** Build while learning — usable MVP in 7–10 days, polished project in 6 weeks
**Time budget:** ~2–3 hrs/day

---

## Timeline at a Glance

| Time | Target |
|---|---|
| Tonight | Repo + DB + dataset |
| Day 3 | Basic ingestion |
| Day 7 | Data-quality engine |
| Day 10 | First working AI agent |
| Week 3 | RAG + root cause analysis |
| Week 4 | Human-approved remediation |
| Week 5 | Production stack |
| Week 6 | Resume + interview preparation |

---

## Day 1 — Setup + Architecture

**Goal:** project skeleton running tonight.

**Stack for now:** Python + PostgreSQL + Docker + Git (nothing else yet)

**Repo structure:**
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
README.md
```

**Today's 3 deliverables:**
- [ ] Create the GitHub repository
- [ ] Create PostgreSQL database with `customers`, `orders`, `payments`, `products`
- [ ] Write a Python script generating ~100k realistic transaction records with deliberately injected data-quality problems (NULLs, duplicates, invalid values, schema changes, missing records, abnormal revenue)

**End of Day 1:** GitHub repo + database + sample data.

---

## Days 2–4 — Data Engineering Foundation

**Build:**
```
API → Python ingestion → PostgreSQL
```
Then add:
```
Kafka → Spark → PostgreSQL/Data Lake
```

Don't touch Kubernetes/Terraform yet.

**Deliverable:** reliable data ingestion and processing.

---

## Days 5–7 — Data Quality Engine

Deterministic checks, built *before* any AI is involved:
- NULL check
- Duplicate check
- Schema check
- Range check
- Freshness check
- Row-count anomaly
- Referential integrity

**Output format:**
```json
{
  "table": "orders",
  "issue": "payment_status_null",
  "severity": "HIGH",
  "affected_rows": 18742
}
```

🎯 **End of Week 1: portfolio-worthy MVP.**

---

## Week 2 — Make It Agentic

Build an agent with tools:
```
             ┌── SQL Tool
             ├── Schema Tool
Agent ───────┼── Data Profiling Tool
             ├── Pipeline Log Tool
             └── Metadata Tool
```

Test case: give it "Revenue dropped 23% today" and have it investigate rather than just answer.

---

## Week 3 — RAG + Root Cause Analysis

Give the agent access to:
- Data dictionaries
- dbt documentation
- Pipeline documentation
- Previous incidents
- Schema history
- Business rules

**Flow:**
```
Anomaly → Agent investigation → RAG + SQL + metadata → Root cause → Confidence score
```

**Example trace:**
Revenue dropped 23% → agent finds `payment_status` is NULL for 18.7% of today's records → searches docs → finds the payment API renamed `paymentStatus` to `payment_status`.

This demonstrates agentic reasoning + RAG + data engineering together — the core interview story.

---

## Week 4 — Autonomous Remediation

Agent generates fixes: SQL updates, ingestion mapping fixes, Kafka replay, dbt reruns, backfills.

**No unrestricted autonomous DB writes.** Use a human-in-the-loop gate:
```
Agent → Proposed Action → Human Approval → Execution → Verification
```

This is a strong interview talking point on its own.

---

## Week 5 — Production Engineering

Add: Docker, Airflow, dbt, Kafka, Spark, FastAPI, logging, monitoring, tests, retries, failure handling.

**Full architecture:**
```
                    ┌──────────────┐
                    │     APIs     │
                    └──────┬───────┘
                           ↓
                        Kafka
                           ↓
                        Spark
                           ↓
                     Data Lake/DB
                           ↓
                          dbt
                           ↓
                    Data Quality
                           ↓
                     ┌────Agent────┐
                     │             │
              SQL Tool       RAG Tool
                     │             │
                     └──────┬──────┘
                            ↓
                     Root Cause
                            ↓
                    Human Approval
                            ↓
                       Remediation
```

---

## Week 6 — Resume / Interview Ready

Not about adding more tech — about being able to defend every choice.

**Data Engineering**
- Why Kafka? Why Spark? Why Airflow?
- Batch vs. streaming?
- How do you handle failures?
- How do you ensure exactly-once / at-least-once processing?
- How would this scale?

**Agentic AI**
- Why an agent instead of a plain LLM call?
- Why LangGraph?
- How does the agent choose which tool to use?
- How do you prevent hallucinations?
- How do you evaluate the agent?
- How does RAG work here?
- What happens when the agent picks the wrong tool?

**Production**
- How would you deploy it?
- How do you monitor it?
- How do you secure database access?
- How do you prevent the agent from running dangerous SQL?

---

## Tracking Docs (keep these updated as you build)

- **CHANGELOG.md** — what changed each session and why
- **PROGRESS.md** — done / in-progress / next, updated every session
- **DECISIONS.md** — why X over Y (libraries, architecture, patterns)
- **README.md** — setup, how to run, project structure
- **PROMPTS_LOG.md** — prompts used for tricky parts + what worked/didn't
- **FAULT_SCENARIOS.md** — data quality issues + detection/remediation + interview talking points
- **Git commits** — commit after each meaningful chunk with clear messages

## Tracking Workflow (MANDATORY - Do this every session)

**Per Session:**
1. Update PROGRESS.md with completed/in-progress items (FIRST action after any work)
2. Update CHANGELOG.md with what changed and why
3. Update DECISIONS.md when choosing technologies (Kafka vs alternatives, Spark vs alternatives, etc.)
4. Log tricky prompts in PROMPTS_LOG.md
5. Commit to Git after meaningful chunks

**As You Build:**
1. Add new fault scenarios to FAULT_SCENARIOS.md as you discover/inject them
2. Update README.md with actual setup instructions as components are built
3. Document schema evolution in DECISIONS.md

**Guardrail:** don't install 15 technologies on Day 1. First 3 days = Python + PostgreSQL + Docker + Git only. Add Kafka → Spark → Airflow/dbt → LangGraph/RAG progressively.