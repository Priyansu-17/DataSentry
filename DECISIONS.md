# Project Decisions

This document tracks key architectural and technology decisions made throughout the project.

## Database
- **PostgreSQL**: Chosen for reliability, strong SQL support, and widespread industry adoption
- **Schema**: customers, orders, payments, products tables for e-commerce transaction data

## Technology Stack (Day 1)
- **Python**: Primary language for data engineering and AI agent development
- **Docker**: Containerization for PostgreSQL
- **Git**: Version control

## Future Decisions (to be documented)
- [ ] Kafka vs. other message brokers
- [ ] Spark vs. other processing engines
- [ ] Airflow vs. other orchestrators
- [ ] LangGraph vs. other agent frameworks
- [ ] Vector database for RAG
