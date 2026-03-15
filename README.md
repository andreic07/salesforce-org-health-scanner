# Salesforce Org Health Scanner

A Python-based CLI tool for analyzing Salesforce org health and security indicators.

The tool connects to Salesforce using the Salesforce CLI and retrieves information via the Salesforce REST API and Tooling API to evaluate common operational and security risks.

---

# Version

Current version: v0.1.0

This initial version provides basic connectivity and the first health checks.

---

# Features

Current checks implemented:

- Salesforce CLI authentication
- Direct Salesforce REST API querying
- System Administrator users check

Planned checks:

- ORG LIMITS usage analysis
- Active Flows health check
- Dangerous permissions detection
- Custom fields explosion detection
- HTML health report generation

---

# Architecture

Project structure:

auth.py → Salesforce CLI authentication  
api.py → Salesforce API communication  
checks.py → Health and security checks  
main.py → CLI entry point  

This structure allows adding new health checks easily without modifying the core logic.

---

# Requirements

- Python 3.10+
- Salesforce CLI
- Access to a Salesforce org

---

# Setup

Create a virtual environment:

python -m venv .venv  
source .venv/bin/activate

---

# Salesforce Authentication

Authorize your Salesforce org using Salesforce CLI:

sf org login web

---

# Running the Scanner

Run the scanner from the project root:

python main.py

You will be prompted to enter the Salesforce org alias.

---


# Roadmap

Upcoming features:

- ORG LIMITS usage analysis
- Active Flows check
- Security permission analysis
- Configurable thresholds
- HTML report generation
- Automated org health scoring

---

# Project Goals

The goal of this project is to provide a lightweight, extensible tool for Salesforce developers and administrators to quickly assess the health and operational risk of a Salesforce org.

---

# License

MIT License