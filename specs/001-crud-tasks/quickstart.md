# Quickstart Guide: Phase 1 In-Memory Todo CLI

**Created**: 2025-12-31
**Purpose**: Help developers quickly understand the codebase and get running locally

## Project Overview

A modular CLI application for managing tasks (Add, View, Update, Delete, Toggle status). Data is stored in-memory and lost on app exit.

**Key Features**:
- Create tasks with auto-assigned unique IDs
- View all tasks in a formatted table
- Update task title/description
- Delete tasks
- Toggle completion status

**Tech Stack**:
- Python 3.13+
- `rich` library for terminal formatting
- `pytest` for testing
- `uv` for dependency management (no global pip)

## Directory Structure

```
todo-app/
├── src/
│   ├── __init__.py
│   ├── models.py           # Task entity definition
│   ├── engine.py           # Business logic (CRUD)
│   ├── interface.py        # CLI menu and formatting
│   └── main.py             # Application entry point
├── tests/
│   ├── test_models.py
│   ├── test_engine.py
│   ├── test_interface.py
│   └── test_integration.py
├── pyproject.toml          # uv project configuration
├── README.md               # Project documentation
└── specs/                  # Feature specifications and design docs
```

## Development Setup

### 1. Clone and Enter Repository

```bash
cd todo-app
```

### 2. Initialize uv Environment

```bash
# Install uv (if not already installed)
# On macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows: PowerShell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment (if not auto-activated)
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### 3. Verify Setup

```bash
python --version  # Should be 3.13+
python -c "import rich; print('rich library OK')"
pytest --version
```

## Running the Application

### Start the App

```bash
python -m src.main
```

### Expected Output

```
╔═══════════════════════════════════════╗
║     Welcome to Todo App Phase 1       ║
╚═══════════════════════════════════════╝

Main Menu:
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Toggle Task Status
  6. Exit

Enter your choice (1-6):
```

## Typical User Workflow

### Step 1: Add a Task

```
Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description: Milk, bread, eggs
✓ Task created with ID 1

Main Menu:
...
```

### Step 2: View Tasks

```
Enter your choice (1-6): 2

Tasks:
┌────┬──────────────────┬──────────────────────┬───────────┐
│ ID │ Title            │ Description          │ Status    │
├────┼──────────────────┼──────────────────────┼───────────┤
│ 1  │ Buy groceries    │ Milk, bread, eggs    │ [ ] Pend. │
└────┴──────────────────┴──────────────────────┴───────────┘

Main Menu:
...
```

### Step 3: Toggle Task Status

```
Enter your choice (1-6): 5
Enter task ID to toggle: 1
✓ Task 1 status changed to Completed

Main Menu:
...
```

### Step 4: Exit App

```
Enter your choice (1-6): 6
Goodbye!
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_engine.py -v
```

### Run Tests with Coverage

```bash
pytest --cov=src tests/
```

### Run a Single Test

```bash
pytest tests/test_engine.py::test_create_task -v
```

## Key Code Locations

### Business Logic Entry Points

**File**: `src/engine.py`
- `create_task(title, description)` - Add a new task
- `get_all_tasks()` - List all tasks
- `update_task(task_id, title=None, description=None)` - Modify task
- `delete_task(task_id)` - Remove task
- `toggle_task_status(task_id)` - Switch Pending ↔ Completed

**File**: `src/models.py`
- `Task` class - Data structure for a single task
- Validation functions for title, description, status

**File**: `src/interface.py`
- `display_menu()` - Show menu and get user choice
- `display_tasks(tasks)` - Format and print task table
- `prompt_task_creation()` - Get title and description from user
- `show_error(message)` - Display error messages

### Application Entry Point

**File**: `src/main.py`
- `main()` - Application event loop
- Calls engine for business logic
- Calls interface for CLI interactions

## Common Tasks for Developers

### Add a New Requirement to a Function

1. Update the spec in `specs/001-crud-tasks/spec.md`
2. Update the function docstring in the relevant module
3. Write tests in `tests/test_*.py`
4. Implement the change
5. Run tests to verify

### Debug a Failing Test

```bash
# Run with verbose output and stop on first failure
pytest tests/test_engine.py::test_create_task -vvs

# Add print statements in test or source code
# Run again to see debug output
```

### Check Code Style

```bash
# Install style checker (one time)
uv pip install flake8 black

# Check style
flake8 src/ tests/

# Auto-format code
black src/ tests/
```

### Add a New Test

1. Create test in `tests/test_*.py` (or add to existing file)
2. Follow naming: `test_<function_name>_<scenario>`
3. Example:

```python
def test_create_task_with_empty_title():
    """Verify that creating a task with empty title raises ValueError."""
    with pytest.raises(ValueError):
        engine.create_task("", "Some description")
```

4. Run the test: `pytest tests/test_engine.py::test_create_task_with_empty_title -v`

## Architecture Overview

### Separation of Concerns

```
User Input
    ↓
interface.py (CLI layer)
    ↓
main.py (orchestration)
    ↓
engine.py (business logic)
    ↓
models.py (data structures)
    ↓
In-Memory Storage (_tasks list)
```

### Data Flow Example: "Add Task"

1. User enters choice "1" → `interface.display_menu()`
2. Menu returns "1" → `main.py` receives choice
3. `main.py` calls `interface.prompt_task_creation()` for input
4. User enters title + description → returns tuple
5. `main.py` calls `engine.create_task(title, description)`
6. `engine.py` validates and stores task in memory
7. Returns new Task object
8. `main.py` calls `interface.show_success()` message
9. Loop continues, menu is displayed again

### Module Independence

- **engine.py**: No imports from interface.py or main.py (pure business logic)
- **models.py**: No imports from engine.py, interface.py, or main.py (pure data)
- **interface.py**: Can import from models.py for type hints; doesn't call engine directly
- **main.py**: Imports all modules; coordinates between interface and engine

## Testing Strategy

### Unit Tests (test_engine.py, test_models.py)

Test individual functions in isolation:

```python
def test_create_task_basic():
    """Verify task creation with basic title and description."""
    task = engine.create_task("Test", "Description")
    assert task["id"] == 1
    assert task["title"] == "Test"
    assert task["status"] == "Pending"
```

### Integration Tests (test_integration.py)

Test full workflows across modules:

```python
def test_add_and_view_tasks():
    """Verify complete workflow: add 2 tasks, view them."""
    engine.create_task("Task 1", "Desc 1")
    engine.create_task("Task 2", "Desc 2")
    tasks = engine.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
```

## Performance Notes

- Linear ID lookup is O(n) → acceptable for 100+ tasks
- Menu loop blocks on user input → expected for CLI
- No database queries → all in-memory, instant
- Table formatting via rich → minimal overhead

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Ensure you're running from the repository root:
```bash
cd /path/to/todo-app
python -m src.main
```

### Issue: "pytest not found"

**Solution**: Ensure uv environment is activated:
```bash
uv sync
source .venv/bin/activate  # or activate.ps1 on Windows
pytest
```

### Issue: "rich not found"

**Solution**: Check pyproject.toml includes rich; re-sync:
```bash
uv sync
```

## Next Steps

1. **Implementation**: Follow `/sp.tasks` for detailed implementation tasks
2. **Testing**: Add tests as you implement each function
3. **Code Review**: Ensure PEP 8 compliance and comprehensive docstrings
4. **QA**: Run quality-tester agent when complete

## Resources

- Python 3.13 Docs: https://docs.python.org/3.13/
- Rich Library: https://rich.readthedocs.io/
- pytest Docs: https://docs.pytest.org/
- PEP 8 Style Guide: https://pep8.org/
- uv Documentation: https://docs.astral.sh/uv/
