# ADR-001: Modular Architecture with Logic-Display Separation

**Status**: Accepted
**Date**: 2025-12-31
**Feature**: 001-crud-tasks (Phase 1 In-Memory Todo CLI)
**Deciders**: Claude Code Agent, Architecture Planning Workflow

## Context

The Phase 1 In-Memory Todo CLI application needs a clear architectural structure that:

- Enables independent testing of business logic without CLI coupling
- Allows future CLI redesigns (web, GUI, API) without touching core logic
- Supports modular development and code review
- Adheres to constitutional principle IV: "Logic-Display Separation"

The codebase will handle CRUD operations (Create, Read, Update, Delete) plus Toggle functionality. Without clear separation, testing becomes difficult, and changes to the UI require modifying business logic.

## Decision

**Organize the application into 4 independent modules with clear dependency flow:**

1. **`models.py`** (Core Data Layer)
   - Defines Task entity structure: id, title, description, status
   - Contains validation functions for field constraints
   - No dependencies on other modules
   - Testable in isolation

2. **`engine.py`** (Business Logic Layer)
   - Implements 6 CRUD operations: create_task, get_all_tasks, get_task_by_id, update_task, delete_task, toggle_task_status
   - Manages in-memory storage (_tasks list, _next_id counter)
   - Handles validation and error states (returns False or raises ValueError)
   - Imports only models.py (for type hints)
   - Pure business logic; no CLI concerns

3. **`interface.py`** (CLI Display Layer)
   - Provides user input prompts (display_menu, prompt_task_creation)
   - Formats output (display_tasks with rich tables, show_error messages)
   - Handles terminal I/O and user interaction
   - Imports models.py for type hints only
   - Does NOT directly call engine functions (orchestration in main.py)

4. **`main.py`** (Orchestration Layer)
   - Application entry point and event loop
   - Coordinates between interface.py (UI) and engine.py (logic)
   - Routes user choices to appropriate engine operations
   - Handles flow control (menu loop, exit conditions)
   - Single responsibility: wire together modules

**Dependency Graph**:
```
main.py → interface.py + engine.py
          ↓               ↓
        models.py ← ← ← ← ↓
```

## Consequences

### Positive

- **Testability**: Business logic in engine.py is completely independent and testable without terminal I/O
  - Unit tests can verify CRUD operations in isolation
  - No mocking of print statements or user input needed for core logic tests
  - Integration tests can test workflows independent of CLI

- **Flexibility**: Future changes to display layer don't affect business logic
  - Could implement web UI (Flask/Django) without changing engine.py
  - Could implement GUI (tkinter/PyQt) without changing engine.py
  - Could implement API (FastAPI) without changing engine.py

- **Code Organization**: Clear separation of concerns
  - Each module has a single, well-defined responsibility
  - Easier for multiple developers to work on different modules simultaneously
  - Easier code review (reviewer knows to focus on logic in engine.py or display in interface.py)

- **Maintainability**: Changes are localized
  - Bug fix in task validation → modify models.py + unit test
  - Bug fix in menu display → modify interface.py + no changes to engine.py
  - New operation (e.g., filter tasks) → add to engine.py, wire in main.py

### Negative

- **Extra Layers**: More files and modules than a monolithic script
  - Slightly more boilerplate code (imports, function calls)
  - Developers new to the codebase must understand 4 files instead of 1
  - Small overhead in function call overhead between layers (negligible)

- **Coupling Between Layers**: While logic is independent, main.py creates coupling
  - Changes to engine.py function signatures require updates in main.py
  - Changes to interface.py signatures require updates in main.py
  - Mitigated by keeping function signatures stable and using the API contracts

- **Initial Setup Complexity**: Modular approach is more complex than inline code
  - Phase 1 scope is small (5 operations); could be written in < 200 lines in a single file
  - Modular approach adds ~400-500 lines across 4 files due to separation and docstrings
  - Justified by future extensibility and testing requirements

## Alternatives Considered

### Alternative 1: Monolithic Single-File Script

**Structure**: Single `main.py` with all code inline (CRUD, UI, orchestration)

**Pros**:
- Simplest to implement for Phase 1
- Fewer files to navigate
- Faster initial development

**Cons**:
- Cannot test business logic without CLI interaction
- Difficult to reuse logic in future web/API implementations
- Hard to isolate and fix bugs (which layer has the issue?)
- Violates constitutional principle IV (Logic-Display Separation)
- Future UI changes require careful surgery in business logic

**Rejected because**: Violates constitutional separation principle; makes future feature reuse impossible; testing becomes tied to CLI

### Alternative 2: Web Framework (Flask/Django) From Start

**Structure**: Use Flask to handle routing, templates for UI, models for data

**Pros**:
- Built-in separation of concerns (MVC)
- Can serve web UI immediately
- Scalable to multiple endpoints

**Cons**:
- Overkill for Phase 1 (CLI-only requirement)
- Requires learning Flask/Django patterns
- Adds development dependencies (much heavier than current setup)
- Violates constitutional constraint: "Single-user In-Memory CLI system"
- Unnecessary complexity for Phase 1 scope

**Rejected because**: Over-engineered for current scope; violates Phase 1 CLI-only constraint; too heavy

### Alternative 3: Plugin Architecture with Pluggable UIs

**Structure**: Core engine + multiple UI plugins (CLI, Web, GUI)

**Pros**:
- Maximum flexibility for future UIs
- Clear separation of concerns
- Could support multiple UIs simultaneously

**Cons**:
- Much more complex than needed for Phase 1
- Requires abstraction layer for UI contracts
- Unnecessary infrastructure overhead
- Delays Phase 1 delivery

**Rejected because**: Over-engineered for Phase 1; introduces complexity that isn't needed yet; can be added in future phases if needed

## Implementation Approach

- Each module is independently testable via pytest
- Engine functions have formal contracts (signatures, behavior, error handling) documented in `contracts/engine_contracts.md`
- Tests organized into unit tests (test_engine.py, test_models.py, test_interface.py) and integration tests (test_integration.py)
- Main.py orchestration is tested via integration tests (end-to-end flows)
- No circular dependencies; flow is one-directional (main → interface/engine → models)

## References

- **Plan**: `specs/001-crud-tasks/plan.md` - Section "Project Structure" and "Key Architectural Decisions #1-5"
- **Data Model**: `specs/001-crud-tasks/data-model.md` - Task entity definition
- **Contracts**: `specs/001-crud-tasks/contracts/engine_contracts.md` - 6 function contracts
- **Constitution**: `.specify/memory/constitution.md` - Principle IV (Logic-Display Separation), Principle VIII (Comprehensive Documentation)

## Notes

This decision enables Phase 2 and beyond to evolve the application without re-architecting the core. The modular approach is intentionally simple (4 layers, not 6+) to avoid over-engineering while still meeting separation and testability requirements.
