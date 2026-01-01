# Implementation Plan: Phase 1 In-Memory Todo CLI

**Branch**: `001-crud-tasks` | **Date**: 2025-12-31 | **Spec**: [Feature Specification](spec.md)
**Input**: Feature specification from `/specs/001-crud-tasks/spec.md`

## Summary

Build a modular in-memory CLI application for core task management (Add, View, Update, Delete, Toggle). Separate business logic from terminal interface to enable independent testing and future CLI redesigns. Use Python 3.13+ managed by `uv` with strict PEP 8 compliance and comprehensive documentation.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: `rich` (terminal formatting and tables)
**Storage**: In-memory list of dictionaries (no persistence)
**Testing**: `pytest` for unit and integration tests
**Target Platform**: Terminal/CLI (cross-platform via Python)
**Project Type**: Single CLI application
**Performance Goals**: All operations complete within 1 second; support 100+ tasks without degradation
**Constraints**: In-memory only; no file persistence; single-user session
**Scale/Scope**: Basic CRUD operations for task management; 5 core features (Add, View, Update, Delete, Toggle)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Alignment

- ✅ **I. Environment & Dependency Management**: Python 3.13+ via `uv` (no global installs)
- ✅ **II. Single-User In-Memory Architecture**: Explicitly in-memory; no persistence
- ✅ **III. Directory Structure Discipline**: `/src` for code, `/specs` for requirements
- ✅ **IV. Logic-Display Separation**: Separate `models.py` (Task entity), `engine.py` (business logic), `interface.py` (CLI display)
- ✅ **V. Strict PEP 8 Adherence**: All code formatted per PEP 8; style enforced in tasks
- ✅ **VI. No Silent Failures**: Try-except wrappers on all user inputs with plain English error messages
- ✅ **VII. Immutability of Scope (Basic Level)**: Only CRUD + Toggle features; no persistence, categories, dates, or filtering
- ✅ **VIII. Comprehensive Documentation**: All functions and classes require docstrings (enforced in implementation)
- ✅ **IX. Specification-Driven Workflow**: Plan follows spec; tasks will follow plan
- ✅ **X. Zero-Touch Human Policy**: All implementation via AI agents (quality-tester gate)
- ✅ **XI. Quality Gate: Agent Audit**: Quality-tester must pass before feature is done
- ✅ **XII. Specification History & Traceability**: Design decisions documented in PHR

**Status**: ✅ PASS - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-crud-tasks/
├── spec.md                    # Feature specification
├── plan.md                    # This file (implementation plan)
├── research.md                # Phase 0 research findings (if needed)
├── data-model.md              # Phase 1: Data entities and relationships
├── quickstart.md              # Phase 1: Developer quickstart
├── contracts/                 # Phase 1: API/function contracts
│   └── engine_contracts.md    # Business logic operation signatures
├── checklists/
│   └── requirements.md        # Quality checklist (completed)
└── tasks.md                   # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models.py                  # Task entity definition and validators
├── engine.py                  # Business logic (CRUD operations)
├── interface.py               # CLI menu, user input, table formatting
├── main.py                    # Application entry point and event loop
└── __init__.py                # Package initialization

tests/
├── test_models.py             # Unit tests for Task entity
├── test_engine.py             # Unit tests for business logic
├── test_interface.py          # Unit tests for CLI formatting
└── test_integration.py        # End-to-end integration tests

pyproject.toml                 # `uv` project configuration
README.md                      # Project documentation
```

**Structure Decision**: Single CLI project (Option 1) with modular separation of concerns. Business logic in `engine.py` is completely independent of CLI in `interface.py`. Task model in `models.py` defines the core entity. Tests are organized by module type (unit vs integration).

## Key Architectural Decisions

### 1. Storage: In-Memory List of Dictionaries

**Decision**: Store tasks in a Python list as dictionaries (or lightweight objects)

**Rationale**:
- Fast lookups by ID (linear search acceptable for 100+ tasks)
- Simple iteration for displaying all tasks
- Native Python data structures (no external DB required)
- Aligns with Phase 1 "in-memory only" constraint

**Tradeoff**:
- Data is temporary (lost on exit) - acceptable per spec
- Linear ID lookup O(n); alternative would be dict by ID (O(1)) but adds complexity
- No persistence strategy needed for Phase 1

**Alternative Considered**: Dictionary indexed by ID for O(1) lookups - rejected (extra complexity, minimal benefit for small datasets)

### 2. ID Management: Global Auto-Incrementing Counter

**Decision**: Maintain a module-level counter that increments on each new task

**Rationale**:
- Guaranteed unique IDs
- Simple to implement
- IDs remain sequential even if tasks are deleted
- Matches user assumption from spec (ID 1, 2, 3...)

**Tradeoff**:
- IDs are never reused (counter only increases) - acceptable per assumption
- No gap-filling on deletion - meets spec requirement for predictable IDs

**Alternative Considered**: Reuse deleted IDs - rejected (complexity and unpredictability)

### 3. Input Validation: Try-Except Wrappers

**Decision**: Wrap all user input operations in try-except blocks with type validation

**Rationale**:
- Prevents crashes from invalid inputs (e.g., non-numeric ID)
- Provides clear error messages in plain English
- Meets constitutional requirement "No Silent Failures"
- Spec requires graceful handling of text instead of numbers

**Tradeoff**:
- Verbose error handling code - necessary for robustness
- Error messages duplicated across multiple operations - can be refactored later

**Alternative Considered**: Single global exception handler - rejected (loses specificity of which operation failed)

### 4. User Interface: Interactive Menu Loop

**Decision**: Display menu, accept choice (1-6 or add/view/update/delete/toggle/exit), execute operation, loop

**Rationale**:
- Simple mental model for users
- Each operation is atomic and independent
- Easy to test each path
- Matches "interactive application" requirement

**Tradeoff**:
- No persistent shell state (user must select operation each time)
- Menu loop blocks on input (acceptable for single-user CLI)

**Alternative Considered**: REPL-style command parsing ("add My Task") - rejected (more complex parsing, less structured)

### 5. Display Formatting: Rich Library

**Decision**: Use `rich` library for formatted tables and styled output

**Rationale**:
- Professional-looking table formatting for task lists
- Status indicator display ([ ] vs [X]) is clean and scannable
- Colors and styling improve UX without major complexity
- Well-maintained library, standard for Python CLI apps

**Tradeoff**:
- External dependency (added to uv project)
- Slightly heavier than plain print statements - acceptable

**Alternative Considered**: Plain print statements - rejected (less professional, harder to read formatted lists)

## Phase 0: Research

No NEEDS CLARIFICATION markers detected in technical context. All architectural decisions are documented above.

**Status**: ✅ COMPLETE (no external dependencies to research; standard Python patterns used)

## Phase 1: Design & Contracts

### Data Model

**Entity: Task**

```python
{
    "id": int,                              # Unique identifier (auto-assigned, sequential)
    "title": str,                           # User-provided task title (non-empty)
    "description": str,                     # User-provided task description (can be empty)
    "status": str                           # "Pending" or "Completed"
}
```

**Validation Rules**:
- `id`: Must be unique; auto-assigned starting from 1
- `title`: Must be non-empty string; max length per Python string limits (no artificial cap)
- `description`: Can be empty string; no length restriction
- `status`: Must be either "Pending" or "Completed"; cannot be other values

**State Transitions**:
- Initial: Created with status "Pending"
- Toggle: Status flips between "Pending" ↔ "Completed"
- Immutable: `id`, `title`, `description` cannot be changed via Toggle (only Update modifies title/description)

### API Contracts

**Module: `engine.py` - Business Logic**

```
Function: create_task(title: str, description: str) -> Task
Purpose: Create a new task with auto-assigned ID and "Pending" status
Input: title (non-empty str), description (str)
Output: Task dict with id, title, description, status="Pending"
Errors: ValueError if title is empty
Test: Create 2 tasks; verify IDs are unique and sequential

Function: get_all_tasks() -> List[Task]
Purpose: Return all tasks in creation order
Input: None
Output: List of Task dicts (empty list if no tasks)
Errors: None (always succeeds)
Test: Add 3 tasks, get_all_tasks() returns 3 items in correct order

Function: get_task_by_id(task_id: int) -> Task | None
Purpose: Retrieve a single task by ID
Input: task_id (int)
Output: Task dict if found, None if not found
Errors: None (returns None for invalid ID)
Test: Add task with ID 1; get_task_by_id(1) returns task; get_task_by_id(999) returns None

Function: update_task(task_id: int, title: str = None, description: str = None) -> bool
Purpose: Update title and/or description of existing task
Input: task_id (int), title (str optional), description (str optional)
Output: True if updated, False if task not found
Errors: ValueError if title is empty (when provided)
Test: Update title; update description; update both; verify other fields unchanged

Function: delete_task(task_id: int) -> bool
Purpose: Remove a task from the system
Input: task_id (int)
Output: True if deleted, False if task not found
Errors: None (returns False for invalid ID)
Test: Delete task; verify it no longer appears in get_all_tasks()

Function: toggle_task_status(task_id: int) -> bool
Purpose: Toggle task status between "Pending" and "Completed"
Input: task_id (int)
Output: True if toggled, False if task not found
Errors: None (returns False for invalid ID)
Test: Toggle pending task → becomes completed; toggle again → becomes pending
```

**Module: `interface.py` - CLI Display**

```
Function: display_menu() -> str
Purpose: Show main menu and return user's choice
Input: None
Output: User-selected option ("1"-"6" or operation name)
Errors: None (loops until valid input)
Test: Display menu; simulate user input; verify correct operation selected

Function: display_tasks(tasks: List[Task]) -> None
Purpose: Format and display all tasks in a table
Input: List of Task dicts
Output: None (prints to console)
Errors: None (handles empty list gracefully)
Test: Display 0 tasks → show "no tasks" message; display 3 tasks → show formatted table with status

Function: prompt_task_creation() -> (str, str)
Purpose: Prompt user for title and description
Input: None
Output: (title, description) tuple
Errors: None (prompts until non-empty title provided)
Test: User input title and description; verify returned tuple is correct

Function: show_error(message: str) -> None
Purpose: Display error message in plain English
Input: Error message string
Output: None (prints to console)
Errors: None
Test: Show error for invalid ID; verify message is user-friendly
```

### Quickstart Guide

See `quickstart.md` for developer setup and local testing.

## Phases of Execution

### Phase 1: Foundation Setup
- Initialize `uv` environment
- Create directory structure (`src/`, `tests/`)
- Set up `pyproject.toml` with dependencies (`pytest`, `rich`)
- Create module files with docstring templates

### Phase 2: Logic Build
- Write `models.py`: Task class/dataclass with validation
- Write `engine.py`: All 6 CRUD operations with error handling
- Write unit tests for engine and models
- Verify all business logic works in isolation

### Phase 3: UI Integration
- Write `interface.py`: Menu, prompts, table formatting
- Write `main.py`: Event loop that ties engine + interface
- Write integration tests for full workflows
- Test error handling with invalid inputs

### Phase 4: QA & Polish
- Code review for PEP 8 compliance
- Test with 0, 5, 50, 100 tasks
- Test all error paths (invalid ID, non-numeric input, etc.)
- Run `quality-tester` agent for final pass/fail verdict

## Next Steps

1. Proceed to `/sp.tasks` to generate implementation tasks
2. Execute `/sp.implement` to write code
3. Run `/quality-tester` for final validation

## Dependencies & Integration Points

- **External**: `rich` library for CLI tables
- **Internal**: No inter-module dependencies (all through `main.py`)
- **Testing**: `pytest` for unit and integration tests

## Risk Analysis

**Risk**: ID counter state lost on app exit (in-memory only)
- Mitigation: Documented in assumptions; expected Phase 1 behavior
- Severity: Low (matches spec requirement)

**Risk**: Large task lists (100+) slow with linear O(n) lookup
- Mitigation: Acceptable for Phase 1; refactor to O(1) dict lookup in Phase 2 if needed
- Severity: Low (performance goal is 1 second, easily met)

**Risk**: Duplicate code for error messages across operations
- Mitigation: Refactor into helper functions (non-blocking improvement)
- Severity: Low (code cleanliness, not functional)

## Complexity Justification

No constitution violations detected. All complexity is justified by functional requirements:
- Modular design (4 modules) required by Logic-Display Separation principle
- Try-except wrappers required by No Silent Failures principle
- Comprehensive docstrings required by Comprehensive Documentation principle
