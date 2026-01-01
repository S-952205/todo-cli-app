<!--
  SYNC IMPACT REPORT
  - Version change: [NONE] → 1.0.0
  - Constitutional initialization with Phase 1 governance
  - Added principles: Structural Mandates, Coding Standards & Integrity, Agentic Workflow Governance, Documentation Standards
  - Templates requiring updates: spec-template.md, plan-template.md, tasks-template.md (all align with Phase 1 scope constraints)
  - Follow-up: None
-->

# Todo CLI App (Phase 1) Constitution

## Core Principles

### I. Environment & Dependency Management
All development MUST be managed via `uv`. No global Python installations are allowed. This ensures reproducible builds and eliminates version conflicts across development machines.

### II. Single-User In-Memory Architecture
The application MUST remain a single-user In-Memory CLI system. Persistence, multi-user support, and distributed state are explicitly out of scope for Phase 1 and require constitutional amendment if needed in future phases.

### III. Directory Structure Discipline
Source code belongs in `/src`. Technical requirements belong in `/specs`. Project context and development guidance belong in `CLAUDE.md`. This strict separation ensures clarity of intent and aids navigation for both humans and agents.

### IV. Logic-Display Separation
Business logic (how the todo works) must be separate from the CLI display logic (how it looks). This isolation enables independent testing of core functionality and easier CLI redesigns without touching business rules.

### V. Strict PEP 8 Adherence
All Python code MUST follow PEP 8 strictly. Variable naming MUST be descriptive and consistent. Readability is non-negotiable; code reviews MUST verify compliance before merge.

### VI. No Silent Failures
Every exception MUST be caught and reported to the user in plain English. Silent failures corrupt user trust and make debugging impossible. All error paths must be explicit and tested.

### VII. Immutability of Scope (Basic Level)
No feature outside the "Basic Level" (Add, View, Update, Delete, Toggle) shall be implemented without a constitutional amendment. This ensures focus and prevents scope creep during Phase 1.

### VIII. Comprehensive Documentation
Every function and class MUST include a docstring explaining its purpose, parameters, and return values. Documentation is not optional; it is a compliance requirement for all code.

### IX. Specification-Driven Workflow
Development MUST strictly follow: `/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement`. This workflow ensures architectural clarity, stakeholder alignment, and traceable decision-making before any code is written.

### X. Zero-Touch Human Policy
The human (user) will not edit any `.py` files. All changes MUST be driven through specifications and AI sub-agents. This ensures consistency and maintains a complete audit trail of all decisions.

### XI. Quality Gate: Agent Audit
No feature is considered "Done" until the `quality-tester` agent issues a formal PASS verdict. This gate prevents incomplete or untested code from entering the project.

### XII. Specification History & Traceability
Specification history MUST be maintained to track why certain logic decisions were made. This aids future refactoring, onboarding, and architectural evolution.

## Governance

### Amendment Procedure
- New principles or scope changes require explicit user consent.
- Constitution changes are tracked in version history with rationale.
- All amendments trigger a review of dependent templates (spec, plan, tasks) to ensure alignment.
- Breaking changes (MAJOR version bumps) require migration planning for existing artifacts.

### Versioning Policy
- **MAJOR**: Backward incompatible governance changes or principle removals.
- **MINOR**: New principles added or materially expanded guidance.
- **PATCH**: Clarifications, wording refinements, typo fixes.

### Compliance Enforcement
- Every PR review MUST verify adherence to applicable principles.
- Complexity or scope creep MUST be justified against constitutional scope (Basic Level only).
- Use `CLAUDE.md` for runtime development guidance; Constitution supersedes all other practices.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
