# Tasks: Phase 1 In-Memory Todo CLI

**Input**: Design documents from `/specs/001-crud-tasks/`
- `spec.md` - Feature requirements and user stories (5 stories, P1+P2 priorities)
- `plan.md` - Architecture and implementation approach (4 modules)
- `data-model.md` - Task entity structure and storage strategy
- `contracts/engine_contracts.md` - Function specifications (6 CRUD operations)

**Execution Order**: Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3-7 (User Stories 1-5 in priority order)

**Organization**: Tasks grouped by user story, enabling independent implementation of each story.

**Testing**: Include unit and integration tests for each story (TDD approach: write tests first, implement second).

---

## Phase 1: Environment Setup (Shared Infrastructure)

**Purpose**: Initialize project structure, dependencies, and development environment
**Duration**: Shared foundational work (all team members)
**Blocker**: Must complete before any user story implementation

### Project Initialization

- [ ] **T001** [P] Create directory structure per plan.md
  - Create `/src/` directory for application code
  - Create `/tests/` directory for test suites
  - Create `/src/__init__.py` (empty package marker)
  - Create `/tests/__init__.py` (empty package marker)
  - **Verification**: `ls -la src/` and `ls -la tests/` show directories exist

- [ ] **T002** Initialize `uv` project with pyproject.toml
  - Create `pyproject.toml` at repository root with:
    - Project name: "todo-cli"
    - Python version: 3.13+
    - Dependencies: `rich` (for table formatting)
    - Dev dependencies: `pytest` (testing), `black` (formatting), `flake8` (linting)
  - Run `uv sync` to lock dependencies
  - **Verification**: `uv sync` succeeds; `.venv/` created with Python 3.13+

- [ ] **T003** [P] Configure code quality tools
  - Create `.flake8` configuration file (max line length 100, ignore E501 for docstrings)
  - Verify `black` can format code: `black --check src/`
  - Verify `flake8` can lint code: `flake8 src/`
  - **Verification**: All quality tools run without errors on empty modules

### Module Templates

- [ ] **T004** [P] Create module files with docstring templates
  - Create `src/models.py` with header docstring and placeholder for Task class
  - Create `src/engine.py` with header docstring and placeholder for CRUD functions
  - Create `src/interface.py` with header docstring and placeholder for CLI functions
  - Create `src/main.py` with header docstring and main() entry point
  - Add `"""Module docstring"""` to each file (PEP 257)
  - **Verification**: All 4 files exist; can import each module without errors

**Checkpoint**: Phase 1 complete ✅
- Project structure ready
- Dependencies installed via uv
- Code quality tools configured
- Module files created with templates

---

## Phase 2: Foundation (Blocking Prerequisites)

**Purpose**: Core data model and engine infrastructure that enables all user stories
**Duration**: Must complete before any user story work
**Blocker**: ALL user story tasks depend on this phase

### Task Entity Model

- [ ] **T005** Create Task entity definition in `src/models.py`
  - Define Task as a Python dict structure (or class with **init**)
  - Include fields: `id` (int), `title` (str), `description` (str), `status` (str)
  - Add type hints for all fields
  - Add docstring: "Represents a single todo item with ID, title, description, and status"
  - **Verification**: `from src.models import Task` works; structure is defined

- [ ] **T006** [P] Add validation functions to `src/models.py`
  - Implement `validate_title(title: str) -> bool` - raise ValueError if empty/whitespace
  - Implement `validate_description(description: str) -> str` - return stripped description
  - Implement `validate_status(status: str) -> bool` - ensure "Pending" or "Completed"
  - Add comprehensive docstrings to each function
  - **Verification**: Functions callable; empty titles raise ValueError; descriptions strip whitespace

### Engine Module Infrastructure

- [ ] **T007** Create module-level state in `src/engine.py`
  - Define `_tasks: List[Dict] = []` - in-memory task storage
  - Define `_next_id: int = 1` - global counter for auto-incrementing IDs
  - Add docstring explaining storage strategy and ID management
  - **Verification**: Module-level variables initialized; can access from tests

- [ ] **T008** [P] Implement helper functions in `src/engine.py`
  - Implement `_get_task_index(task_id: int) -> int` - return index of task in _tasks list, -1 if not found
  - Implement `_reset_state() -> None` - reset _tasks and _next_id to initial state (testing only)
  - Add docstrings to both functions
  - **Verification**: Helper functions work correctly; _reset_state clears all data

### CLI Interface Infrastructure

- [ ] **T009** [P] Create utility functions in `src/interface.py`
  - Implement `show_message(message: str) -> None` - print message to console
  - Implement `show_error(message: str) -> None` - print error in red/bold format using rich
  - Implement `show_success(message: str) -> None` - print success message in green using rich
  - Add docstrings to each function
  - **Verification**: Functions print formatted output to console; colors display correctly

- [ ] **T010** [P] Create input handling in `src/interface.py`
  - Implement `prompt_string(prompt_text: str, required: bool = False) -> str` - get string input with validation
  - Implement `prompt_integer(prompt_text: str) -> int | None` - get integer input, return None if invalid
  - Add error handling with try-except; show user-friendly messages
  - Add docstrings
  - **Verification**: Functions accept valid input; reject invalid input gracefully with error messages

### Main Application Setup

- [ ] **T011** Create main() event loop skeleton in `src/main.py`
  - Implement `main()` function with while True loop
  - Display menu and get user choice
  - Stub out operation handlers (if-elif for each choice)
  - Add docstring explaining event loop
  - **Verification**: `python -m src.main` runs; menu displays; accepts user input (handler is stub)

**Checkpoint**: Phase 2 complete ✅
- Task entity model defined with validation
- Engine module state initialized
- Helper functions for CLI created
- Main event loop structure established
- ALL user story work can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can create a new task with title and description; system auto-assigns ID and sets status to "Pending"

**Independent Test**: Launch app → Select "Add Task" → Enter title and description → Task appears in list with unique ID and "Pending" status

### Tests for User Story 1 (TDD: Write tests FIRST)

- [ ] **T012** [P] [US1] Unit test: `test_create_task_basic()` in `tests/test_engine.py`
  - Test: `engine.create_task("Buy milk", "From the store")` returns task with ID, title, description, status="Pending"
  - Assert: `task["id"] == 1`, `task["title"] == "Buy milk"`, `task["status"] == "Pending"`
  - **Verification**: Test written; pytest runs it; test FAILS (function not implemented yet)

- [ ] **T013** [P] [US1] Unit test: `test_create_task_id_uniqueness()` in `tests/test_engine.py`
  - Test: Create 2 tasks; verify IDs are unique and sequential (1, then 2)
  - Assert: `task1["id"] == 1`, `task2["id"] == 2`, `task1["id"] != task2["id"]`
  - **Verification**: Test written; FAILS before implementation

- [ ] **T014** [P] [US1] Unit test: `test_create_task_empty_title_rejected()` in `tests/test_engine.py`
  - Test: `engine.create_task("", "desc")` raises ValueError
  - Use `pytest.raises(ValueError)`
  - **Verification**: Test written; FAILS before implementation

- [ ] **T015** [P] [US1] Integration test: `test_add_task_via_interface()` in `tests/test_integration.py`
  - Test: Simulate user input (title="Test", description="Desc")
  - Call interface function to prompt (or mock input)
  - Call engine.create_task()
  - Verify task appears in engine.get_all_tasks()
  - **Verification**: Test written; FAILS before implementation

### Implementation for User Story 1

- [ ] **T016** Implement `create_task()` function in `src/engine.py`
  - Signature: `def create_task(title: str, description: str = "") -> dict`
  - Validate title (non-empty, strip whitespace) - raise ValueError if invalid
  - Create task dict with auto-assigned ID (use _next_id)
  - Set status to "Pending"
  - Append to _tasks list
  - Increment _next_id
  - Return task dict
  - Add comprehensive docstring with examples
  - **Verification**: `pytest tests/test_engine.py::test_create_task_*` all PASS

- [ ] **T017** [P] Implement prompt function in `src/interface.py` for task creation
  - Implement `prompt_task_creation() -> (str, str)` - returns (title, description) tuple
  - Prompt user for title (required, non-empty)
  - Prompt user for description (optional, can be empty)
  - Add docstring
  - **Verification**: Function prompts user; accepts input; returns tuple

- [ ] **T018** Wire "Add Task" operation in `src/main.py`
  - In main() event loop, handle choice "1" or "add"
  - Call `interface.prompt_task_creation()` to get input
  - Call `engine.create_task(title, description)` to create task
  - Call `interface.show_success()` with created task ID
  - Add try-except for error handling (ValueError caught, error message shown)
  - Add docstring to handler function
  - **Verification**: `python -m src.main` → Choose "1" → Enter title/desc → Task created and message displayed

- [ ] **T019** [P] Code review and PEP 8 compliance for US1
  - Run `black src/ tests/` to auto-format code
  - Run `flake8 src/models.py src/engine.py src/interface.py` to check style
  - Ensure all docstrings follow PEP 257
  - **Verification**: `flake8` returns no errors; `black` shows no changes needed

**Checkpoint**: User Story 1 complete ✅
- Create operation fully implemented and tested
- Tests pass: `pytest tests/test_engine.py -k create`
- Can run app and add tasks
- Code is PEP 8 compliant with docstrings

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all tasks in a formatted list with ID, title, status indicator, and description

**Independent Test**: Add 2+ tasks → Select "View Tasks" → All tasks displayed in formatted table with status `[ ]` for pending and `[X]` for completed

### Tests for User Story 2 (TDD: Write tests FIRST)

- [ ] **T020** [P] [US2] Unit test: `test_get_all_tasks_basic()` in `tests/test_engine.py`
  - Test: Create 2 tasks; call `engine.get_all_tasks()` → returns list with 2 tasks in order
  - Assert: `len(tasks) == 2`, `tasks[0]["title"] == first_title`, `tasks[1]["title"] == second_title`
  - **Verification**: Test written; FAILS before implementation

- [ ] **T021** [P] [US2] Unit test: `test_get_all_tasks_empty()` in `tests/test_engine.py`
  - Test: No tasks created; call `engine.get_all_tasks()` → returns empty list
  - Assert: `get_all_tasks() == []`
  - **Verification**: Test written; FAILS before implementation

- [ ] **T022** [P] [US2] Integration test: `test_view_tasks_displays_table()` in `tests/test_integration.py`
  - Test: Create 2 tasks; call interface function to display tasks
  - Verify output contains task titles and status indicators
  - **Verification**: Test written; FAILS before implementation

### Implementation for User Story 2

- [ ] **T023** Implement `get_all_tasks()` function in `src/engine.py`
  - Signature: `def get_all_tasks() -> list`
  - Return copy of _tasks list (or list itself; read-only operation)
  - Return empty list if _tasks is empty
  - Add comprehensive docstring
  - **Verification**: `pytest tests/test_engine.py::test_get_all_tasks_*` all PASS

- [ ] **T024** [P] Implement display function in `src/interface.py` for task list
  - Implement `display_tasks(tasks: list) -> None` - format and print all tasks
  - Use `rich.table.Table` to create formatted table
  - Include columns: ID, Title, Status, Description
  - Status display: "[ ] Pending" or "[X] Completed"
  - If no tasks: print "No tasks exist"
  - Add docstring
  - **Verification**: Function displays formatted table; status shows correctly

- [ ] **T025** Wire "View Tasks" operation in `src/main.py`
  - In main() event loop, handle choice "2" or "view"
  - Call `engine.get_all_tasks()` to retrieve all tasks
  - Call `interface.display_tasks(tasks)` to format and display
  - Add docstring to handler function
  - **Verification**: `python -m src.main` → Choose "2" → Tasks displayed in table format

- [ ] **T026** [P] Code review and PEP 8 compliance for US2
  - Run `black src/ tests/` to auto-format
  - Run `flake8` to check style
  - Ensure docstrings are complete
  - **Verification**: No style errors; all docstrings present

**Checkpoint**: User Story 2 complete ✅
- View operation fully implemented and tested
- Tests pass: `pytest tests/test_engine.py -k get_all`
- Can run app and view tasks in formatted table
- Code is PEP 8 compliant

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: Users can modify title and/or description of an existing task by ID

**Independent Test**: Create task → Select "Update Task" → Provide ID and new title/description → Changes appear when viewing tasks

### Tests for User Story 3 (TDD: Write tests FIRST)

- [ ] **T027** [P] [US3] Unit test: `test_update_task_title()` in `tests/test_engine.py`
  - Create task; call `engine.update_task(task_id=1, title="New Title")`
  - Assert: Returns True; task title changed; description unchanged
  - **Verification**: Test written; FAILS before implementation

- [ ] **T028** [P] [US3] Unit test: `test_update_task_description()` in `tests/test_engine.py`
  - Create task; call `engine.update_task(task_id=1, description="New Desc")`
  - Assert: Returns True; description changed; title unchanged
  - **Verification**: Test written; FAILS before implementation

- [ ] **T029** [P] [US3] Unit test: `test_update_task_not_found()` in `tests/test_engine.py`
  - Call `engine.update_task(task_id=999, title="Anything")`
  - Assert: Returns False (task not found)
  - **Verification**: Test written; FAILS before implementation

- [ ] **T030** [P] [US3] Unit test: `test_update_task_empty_title_rejected()` in `tests/test_engine.py`
  - Call `engine.update_task(task_id=1, title="")` → raises ValueError
  - **Verification**: Test written; FAILS before implementation

### Implementation for User Story 3

- [ ] **T031** Implement `update_task()` function in `src/engine.py`
  - Signature: `def update_task(task_id: int, title: str = None, description: str = None) -> bool`
  - Find task by ID using helper function
  - If not found: return False
  - If title provided: validate and update (raise ValueError if empty)
  - If description provided: validate and update
  - Return True if updated
  - Add comprehensive docstring
  - **Verification**: `pytest tests/test_engine.py::test_update_task_*` all PASS

- [ ] **T032** [P] Implement prompt functions in `src/interface.py` for update operation
  - Implement `prompt_task_id() -> int | None` - prompt for task ID, return None if invalid
  - Implement `prompt_update_fields() -> (str | None, str | None)` - prompt for new title/description
  - Add error handling for non-numeric input
  - Add docstrings
  - **Verification**: Functions handle invalid input gracefully

- [ ] **T033** Wire "Update Task" operation in `src/main.py`
  - Handle choice "3" or "update"
  - Call prompt functions to get task ID and new fields
  - Call `engine.update_task(task_id, title, description)`
  - Show success or error message
  - Add try-except for ValueError handling
  - Add docstring
  - **Verification**: `python -m src.main` → Choose "3" → Update task successfully

- [ ] **T034** [P] Code review and PEP 8 compliance for US3
  - Run `black` and `flake8`
  - Verify docstrings complete
  - **Verification**: No style errors

**Checkpoint**: User Story 3 complete ✅
- Update operation implemented and tested
- Tests pass: `pytest tests/test_engine.py -k update`
- Code is PEP 8 compliant

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: Users can remove a task from the system by ID

**Independent Test**: Create task → Select "Delete Task" → Provide ID → Task no longer appears in list

### Tests for User Story 4 (TDD: Write tests FIRST)

- [ ] **T035** [P] [US4] Unit test: `test_delete_task_success()` in `tests/test_engine.py`
  - Create task; call `engine.delete_task(task_id=1)`
  - Assert: Returns True; task no longer in `get_all_tasks()`
  - **Verification**: Test written; FAILS before implementation

- [ ] **T036** [P] [US4] Unit test: `test_delete_task_not_found()` in `tests/test_engine.py`
  - Call `engine.delete_task(task_id=999)`
  - Assert: Returns False
  - **Verification**: Test written; FAILS before implementation

- [ ] **T037** [P] [US4] Unit test: `test_delete_task_id_not_reused()` in `tests/test_engine.py`
  - Create task (ID=1); delete task (ID=1); create new task
  - Assert: New task gets ID=2, not ID=1
  - **Verification**: Test written; FAILS before implementation

### Implementation for User Story 4

- [ ] **T038** Implement `delete_task()` function in `src/engine.py`
  - Signature: `def delete_task(task_id: int) -> bool`
  - Find task index by ID
  - If not found: return False
  - Remove task from _tasks list
  - Return True
  - Note: _next_id counter unchanged (IDs not reused)
  - Add comprehensive docstring
  - **Verification**: `pytest tests/test_engine.py::test_delete_task_*` all PASS

- [ ] **T039** Wire "Delete Task" operation in `src/main.py`
  - Handle choice "4" or "delete"
  - Prompt for task ID
  - Call `engine.delete_task(task_id)`
  - Show success or "task not found" message
  - Add docstring
  - **Verification**: `python -m src.main` → Choose "4" → Delete task successfully

- [ ] **T040** [P] Code review and PEP 8 compliance for US4
  - Run `black` and `flake8`
  - **Verification**: No style errors

**Checkpoint**: User Story 4 complete ✅
- Delete operation implemented and tested
- Tests pass: `pytest tests/test_engine.py -k delete`
- Code is PEP 8 compliant

---

## Phase 7: User Story 5 - Toggle Task Status (Priority: P2)

**Goal**: Users can mark a task as completed or revert it to pending by toggling status

**Independent Test**: Create task (Pending) → Select "Toggle" → Status becomes "Completed" → Toggle again → Status becomes "Pending"

### Tests for User Story 5 (TDD: Write tests FIRST)

- [ ] **T041** [P] [US5] Unit test: `test_toggle_task_status_pending_to_completed()` in `tests/test_engine.py`
  - Create task (status="Pending"); call `engine.toggle_task_status(task_id=1)`
  - Assert: Returns True; status is now "Completed"
  - **Verification**: Test written; FAILS before implementation

- [ ] **T042** [P] [US5] Unit test: `test_toggle_task_status_completed_to_pending()` in `tests/test_engine.py`
  - Create and toggle task to "Completed"; toggle again
  - Assert: Returns True; status is now "Pending"
  - **Verification**: Test written; FAILS before implementation

- [ ] **T043** [P] [US5] Unit test: `test_toggle_task_status_not_found()` in `tests/test_engine.py`
  - Call `engine.toggle_task_status(task_id=999)`
  - Assert: Returns False
  - **Verification**: Test written; FAILS before implementation

### Implementation for User Story 5

- [ ] **T044** Implement `toggle_task_status()` function in `src/engine.py`
  - Signature: `def toggle_task_status(task_id: int) -> bool`
  - Find task by ID
  - If not found: return False
  - Toggle status: "Pending" → "Completed" or vice versa
  - Return True
  - Add comprehensive docstring
  - **Verification**: `pytest tests/test_engine.py::test_toggle_task_status_*` all PASS

- [ ] **T045** Wire "Toggle Task Status" operation in `src/main.py`
  - Handle choice "5" or "toggle"
  - Prompt for task ID
  - Call `engine.toggle_task_status(task_id)`
  - Show success or "task not found" message
  - Add docstring
  - **Verification**: `python -m src.main` → Choose "5" → Toggle task successfully

- [ ] **T046** [P] Code review and PEP 8 compliance for US5
  - Run `black` and `flake8`
  - **Verification**: No style errors

**Checkpoint**: User Story 5 complete ✅
- Toggle operation implemented and tested
- Tests pass: `pytest tests/test_engine.py -k toggle`
- Code is PEP 8 compliant

---

## Phase 8: Menu and Exit Functionality

**Goal**: Complete main.py event loop with proper menu handling and exit

### Implementation

- [ ] **T047** [P] Complete menu display in `src/interface.py`
  - Implement `display_menu() -> str` - show menu options 1-6, get user choice
  - Validate choice (1-6 or "add"/"view"/"update"/"delete"/"toggle"/"exit")
  - Reprompt on invalid choice
  - Handle case-insensitivity
  - Add docstring
  - **Verification**: Menu displays; accepts valid choices; rejects invalid

- [ ] **T048** Complete main.py event loop
  - Implement all if-elif-else branches in main() for each menu choice
  - Wire all 5 user story handlers (Add, View, Update, Delete, Toggle)
  - Implement "6" or "exit" choice to break loop and exit cleanly
  - Add welcome message at startup
  - Add goodbye message at exit
  - Add docstring to main()
  - **Verification**: `python -m src.main` → All menu options work; exit gracefully

**Checkpoint**: Complete application loop ✅
- All 6 menu options functional
- App can be launched and exited cleanly
- All CRUD operations integrated

---

## Phase 9: Integration Testing and Workflow Validation

**Goal**: Verify complete workflows from user perspective; ensure all features work together

### End-to-End Testing

- [ ] **T049** [P] Write end-to-end integration test in `tests/test_integration.py`
  - Test scenario: Add task → View task → Update task → Toggle status → Delete task
  - Verify state after each operation
  - Verify task appears/disappears from list correctly
  - Add docstring
  - **Verification**: `pytest tests/test_integration.py::test_*` all PASS

- [ ] **T050** [P] Test error paths and edge cases in `tests/test_integration.py`
  - Test: Non-numeric ID input → error message shown
  - Test: Empty task list → "no tasks" message shown
  - Test: Update non-existent task → "not found" message shown
  - Test: Delete non-existent task → "not found" message shown
  - **Verification**: All error paths tested and handled gracefully

- [ ] **T051** [P] Test boundary conditions in `tests/test_integration.py`
  - Test: Create task with very long title (1000+ chars) → stored and displayed
  - Test: Create task with empty description → stored and displayed
  - Test: Create and delete all tasks → system resets to empty state
  - **Verification**: All boundary conditions handled

### Manual Testing

- [ ] **T052** Manual end-to-end workflow test
  - Launch app: `python -m src.main`
  - Add 3 tasks with various titles and descriptions
  - View tasks → verify formatting, status indicators
  - Update task title → view and verify change
  - Toggle task status → view and verify change
  - Delete task → view and verify task is gone
  - Verify remaining tasks still present with correct IDs
  - Exit app cleanly
  - **Verification**: All operations work; data consistency maintained

**Checkpoint**: Integration testing complete ✅
- End-to-end workflows validated
- Error paths tested
- Edge cases handled
- Manual testing passed

---

## Phase 10: Code Quality and Final Polish

**Goal**: Ensure code meets all quality standards before QA audit

### Code Formatting and Linting

- [ ] **T053** [P] Format all code with Black
  - Run `black src/ tests/` to auto-format all Python files
  - Verify all files follow Black style (line length 88)
  - **Verification**: `black --check src/ tests/` shows no changes needed

- [ ] **T054** [P] Lint all code with Flake8
  - Run `flake8 src/ tests/` to check style violations
  - Fix any violations (unused imports, long lines, etc.)
  - **Verification**: `flake8 src/ tests/` returns exit code 0 (no errors)

### Documentation

- [ ] **T055** [P] Verify all docstrings are complete and accurate
  - Check every function has docstring (PEP 257 format)
  - Docstrings include: purpose, args, return type, raises, examples
  - Check all module files have header docstrings
  - **Verification**: All docstrings present and accurate; `flake8` finds no docstring issues

- [ ] **T056** [P] Verify all constants and complex logic have comments
  - Add inline comments for non-obvious logic
  - No need for trivial assignments; focus on "why" not "what"
  - **Verification**: Code is readable and well-commented

### Test Coverage

- [ ] **T057** [P] Verify test coverage with pytest
  - Run `pytest tests/ --cov=src` to measure code coverage
  - Aim for >90% coverage of engine.py (most critical logic)
  - Aim for >80% coverage of interface.py and models.py
  - **Verification**: Coverage report shows adequate coverage

- [ ] **T058** [P] Run full test suite
  - Run `pytest tests/ -v` to execute all tests
  - Verify all tests PASS (no skips, no failures)
  - **Verification**: `pytest` exit code 0; all tests passing

### Final Quality Checklist

- [ ] **T059** [P] Final code quality review checklist
  - [ ] All functions have docstrings (PEP 257)
  - [ ] All code formatted with Black (no style violations)
  - [ ] All code passes Flake8 (no linting issues)
  - [ ] All tests pass (pytest exit code 0)
  - [ ] No silent failures (all errors caught and reported)
  - [ ] Logic-display separation maintained (engine.py independent of interface.py)
  - [ ] In-memory storage working (data lost on exit, as expected)
  - [ ] All 5 CRUD operations fully functional
  - [ ] Error messages are user-friendly (plain English, not stack traces)
  - **Verification**: All checklist items verified

**Checkpoint**: Code quality complete ✅
- All code formatted and linted
- All docstrings complete
- >80% test coverage
- All tests passing
- Ready for QA audit

---

## Phase 11: QA Audit and Final Validation

**Goal**: Independent quality validation via quality-tester agent

### Quality Assurance Execution

- [ ] **T060** Execute quality-tester agent audit
  - Run `/quality-tester` agent to perform comprehensive QA
  - Agent will validate:
    - All features work per spec (5 user stories)
    - All requirements met (12 functional requirements)
    - All success criteria satisfied (8 measurable outcomes)
    - Code quality (PEP 8, docstrings, organization)
    - Error handling (no crashes, user-friendly messages)
    - Edge cases handled
  - **Verification**: quality-tester returns PASS verdict

- [ ] **T061** Address any QA failures
  - If quality-tester identifies failures, document in issue
  - Fix issues and re-run quality-tester
  - Repeat until PASS verdict
  - **Verification**: quality-tester returns PASS; all issues resolved

- [ ] **T062** Final sign-off
  - Verify quality-tester PASS verdict
  - Confirm all tasks completed
  - Mark feature as "DONE"
  - **Verification**: Feature ready for delivery

**Final Checkpoint**: Feature Complete ✅
- Quality-tester PASS verdict issued
- All 5 user stories implemented and tested
- All 12 functional requirements met
- All 8 success criteria satisfied
- Code is production-ready

---

## Task Summary

**Total Tasks**: 62
**Organization**:
- Phase 1: 4 tasks (Setup)
- Phase 2: 7 tasks (Foundation)
- Phase 3-7: 40 tasks (User Stories 1-5 with tests + implementation + code review)
- Phase 8: 2 tasks (Menu/Exit)
- Phase 9: 3 tasks (Integration Testing)
- Phase 10: 7 tasks (Code Quality)
- Phase 11: 3 tasks (QA Audit)

**Execution Flow**:
1. Complete Phase 1 (Setup) first
2. Complete Phase 2 (Foundation) - all stories depend on this
3. Execute Phases 3-7 in parallel (each story is independent)
4. Execute Phases 8-11 sequentially

**Success Criteria**:
- All 62 tasks marked ✅ complete
- quality-tester agent issues PASS verdict
- Code passes all linting and formatting checks
- All tests passing (pytest exit code 0)
- All 5 user stories fully functional
- All error paths handled gracefully

---

## Notes

- **TDD Approach**: Each phase includes "write tests first" for unit and integration tests
- **Parallel Work**: Most tasks marked [P] can run in parallel after Phase 2 foundation is complete
- **Code Quality**: PEP 8 compliance and comprehensive docstrings are required for all code
- **Testing**: >80% test coverage required before QA audit
- **Zero Silent Failures**: All errors must be caught and reported in plain English to user
