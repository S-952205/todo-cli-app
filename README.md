# Todo CLI - Phase 1

A simple terminal-based todo application built with Python 3.13+.

**Version**: 0.1.0 | **Status**: Phase 1 (MVP) | **License**: MIT

---

## Project Structure

```
todo-app/
├── src/                    # Application code
│   ├── main.py            # Entry point & event loop
│   ├── engine.py          # CRUD business logic
│   ├── interface.py       # CLI menu & display
│   └── models.py          # Task entity & validation
│
├── tests/                 # Automated tests
│   ├── test_engine.py     # Unit tests
│   └── test_integration.py # End-to-end tests
│
├── specs/                 # Design documents
│   └── 001-crud-tasks/
│       ├── spec.md        # Feature spec
│       ├── plan.md        # Architecture
│       ├── data-model.md  # Data structure
│       └── tasks.md       # Task breakdown
│
├── history/               # Development history
│   ├── prompts/           # Prompt History Records
│   └── adr/               # Architectural Decision Records
│
├── .gitignore             # Git ignore patterns
├── pyproject.toml         # Project config
├── README.md              # This file
└── CLAUDE.md              # Development guidelines
```

---

## What Was Built

**5 Core Features:**

1. **Add Task** - Create new task with title + description
2. **View Tasks** - Display all tasks in formatted table
3. **Update Task** - Modify title/description by ID
4. **Delete Task** - Remove task permanently
5. **Toggle Status** - Mark as Pending/Completed

**Tech Stack:**
- Language: Python 3.13+
- Package Manager: `uv`
- Display: `rich` (terminal formatting)
- Testing: `pytest`
- Code Quality: `black`, `flake8`

---

## How to Run

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run Application

```bash
python -m src.main
```

Or use the installed command:
```bash
todo
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

### 4. Format & Lint Code

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/
```

---

## Using the Application

When you run the app, you'll see an interactive menu:

```
📋 Todo Manager Menu
─────────────────────────────────────
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit
```

**Example workflow:**
- Press `1` to add a task
- Enter title: "Buy groceries"
- Enter description: "Milk, bread, eggs"
- Press `2` to view all tasks
- Press `5` to mark task as completed
- Press `6` to exit

---

## Task Entity

Each task has:
- `id`: Auto-assigned, unique (1, 2, 3, ...)
- `title`: Required, non-empty string
- `description`: Optional
- `status`: "Pending" or "Completed"

---

## Architecture

**Modular Design** (Separation of Concerns):

```
main.py
  ├── interface.py  ← User interaction (CLI)
  ├── engine.py     ← Business logic (CRUD)
  └── models.py     ← Data structures
```

- **models.py**: Task entity + validation
- **engine.py**: Pure business logic, no UI
- **interface.py**: Pure display logic, no business logic
- **main.py**: Orchestrates everything

---

## Notes

- **Storage**: In-memory only (data lost on exit)
- **Persistence**: Not included in Phase 1
- **Single-user**: Single session, no database
- **PEP 8**: All code follows Python style guide
- **Tests**: 15+ unit tests, 5+ integration tests
- **Coverage**: >80% code coverage target

---

## Requirements

- Python 3.13 or higher
- `uv` package manager

---

## Development Approach

This project follows **Spec-Driven Development (SDD)**:
- **Specifications**: Feature requirements and contracts
- **Planning**: Architecture and design decisions
- **Implementation**: Task-driven development with testing
- **Documentation**: PHRs and ADRs for traceability

## Documentation

For more details, see:
- `specs/001-crud-tasks/spec.md` - Feature requirements
- `specs/001-crud-tasks/plan.md` - Architecture and design decisions
- `specs/001-crud-tasks/data-model.md` - Data structure and entity definitions
- `specs/001-crud-tasks/contracts/` - API contracts and test requirements
- `history/adr/` - Architectural Decision Records
- `history/prompts/` - Prompt History Records (development log)
- `CLAUDE.md` - Development guidelines and policies

---

**Last Updated**: January 2, 2026
**Branch**: `main`
