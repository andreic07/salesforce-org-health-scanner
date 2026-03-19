# Salesforce Org Health Scanner

A Python-based CLI tool for analyzing Salesforce org health, security, and automation complexity.

The tool connects to Salesforce using the Salesforce CLI and retrieves data via the Salesforce REST API and Tooling API to evaluate operational risks, system limits, and automation patterns.

---

# Version

Current version: v0.2.0

This version introduces multiple health checks and improved project structure.

---

# Features

## Implemented checks

- Salesforce CLI authentication
- Direct Salesforce REST API querying
- System Administrator users analysis
- ORG LIMITS usage analysis
- Active Flows analysis

---

## System Administrator Check

Identifies active users with System Administrator profile and evaluates risk based on count.

---

## ORG LIMITS

The scanner retrieves limits from the Salesforce Limits API and evaluates current usage with warning thresholds.

Features:

- Retrieves limits via REST API
- Calculates usage percentage
- Displays warning and critical thresholds

---

## Active Flows

The scanner analyzes Salesforce Flows using the Tooling API to provide insights into automation complexity and flow usage.

Features:

- Retrieves flow definitions and versions via Tooling API
- Identifies active and inactive flows
- Calculates total number of versions per flow
- Displays last modified date in user-friendly format
- Provides overview of flows by process type
- Evaluates automation complexity based on number of active flows

---

# Architecture

Project structure:

sf_health_scanner/
    auth.py                # Salesforce CLI authentication
    api.py                 # Salesforce API communication
    checks/
        system_admin_check.py   # Admin analysis
        limits_check.py         # ORG LIMITS analysis
        flows_check.py          # Flow analysis

main.py                    # CLI entry point

This modular structure allows adding new health checks easily without modifying the core logic.

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

Install dependencies:

pip install httpx

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

- Dangerous permissions detection
- Custom fields explosion detection
- Configurable thresholds
- HTML report generation
- Automated org health scoring
- Flow object mapping (advanced analysis)

---

# Project Goals

The goal of this project is to provide a lightweight, extensible tool for Salesforce developers and administrators to quickly assess the health, security, and automation complexity of a Salesforce org.

---

# License

MIT License
