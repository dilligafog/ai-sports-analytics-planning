---
id: ADH-020
title: Playbook Project Setup
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-020-playbook-project-setup
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Step 1 — Project Setup & Structure

**Feature:** Project Initialization  
**Value:** A clean and standardized project structure ensures that all contributors, tools, and future features work off the same foundation. It reduces confusion and prevents rework later.

## Steps
1. **Context** – At the beginning, we need a baseline project structure so data, models, and scripts don’t end up scattered.  
2. **Implementation** –  
   - Initialize the project root.  
   - Create directories: `data/raw`, `data/gold`, `src/`, `notebooks/`, `tests/`.  
   - Add config files (`settings.py`, `.env`, `requirements.txt`).  
   - Set up Git for version control.  
3. **Validation** – Verify you can run a simple test command (`busta --help`) and that the folder structure matches expectations.  
4. **Next Impact** – Provides a clean base so that when we add data sources and features, they have a consistent home and don’t break the project layout.
