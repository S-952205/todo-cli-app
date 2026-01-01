# Engine API Contracts: Phase 1 In-Memory Todo CLI

**Created**: 2025-12-31
**Module**: `src/engine.py`
**Purpose**: Formal specification of business logic function signatures and behavior

## Overview

The `engine.py` module provides all business logic operations for task management. These functions are independent of the CLI interface and can be tested in isolation.

## Function: `create_task`

### Signature

```python
def create_task(title: str, description: str = "") -> dict:
    """
    Create a new task with auto-assigned ID and 'Pending' status.

    Args:
        title: Non-empty task title
        description: Optional task description (default: empty string)

    Returns:
        Task dict with keys: id, title, description, status

    Raises:
        ValueError: If title is empty or only whitespace

    Example:
        >>> task = create_task("Buy milk", "From the store")
        >>> task
        {'id': 1, 'title': 'Buy milk', 'description': 'From the store', 'status': 'Pending'}
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Input Validation** | Title must be non-empty (raises ValueError if empty or whitespace-only) |
| **ID Assignment** | Automatically assigned; next available from global counter |
| **Status** | Always set to "Pending" for new tasks |
| **Order** | Task added to end of internal list (insertion order preserved) |
| **Side Effect** | Increments global counter; modifies internal _tasks list |
| **Idempotent** | No (each call creates a new unique task) |
| **Thread Safe** | No (not required for Phase 1) |

### Test Cases

```python
# TC-create-01: Basic creation
create_task("Buy groceries", "Milk and bread")
→ Returns task with id=1, status="Pending"

# TC-create-02: Empty description allowed
create_task("Review PR", "")
→ Returns task with empty description field

# TC-create-03: ID is unique and sequential
create_task("Task 1", "")  # id=1
create_task("Task 2", "")  # id=2
→ IDs are 1 and 2 (sequential, no duplicates)

# TC-create-04: Empty title rejected
create_task("", "Description")
→ Raises ValueError

# TC-create-05: Whitespace-only title rejected
create_task("   ", "Description")
→ Raises ValueError (after stripping)

# TC-create-06: Title is stripped
create_task("  Task  ", "")
→ Stored as "Task" (leading/trailing whitespace removed)
```

---

## Function: `get_all_tasks`

### Signature

```python
def get_all_tasks() -> list:
    """
    Retrieve all tasks from the system.

    Returns:
        List of Task dicts in insertion order (creation order)
        Empty list if no tasks exist

    Example:
        >>> get_all_tasks()
        [
            {'id': 1, 'title': 'Task 1', 'description': '', 'status': 'Pending'},
            {'id': 2, 'title': 'Task 2', 'description': 'Details', 'status': 'Completed'}
        ]
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Return Order** | Insertion order (tasks in creation sequence) |
| **Empty List** | Returns [] if no tasks exist (no error) |
| **Modification** | Returns shallow copy (modifications to list don't affect internal state) |
| **Search** | No filtering or sorting (all tasks returned) |
| **Side Effect** | None (read-only operation) |
| **Idempotent** | Yes (same input → same output) |
| **Thread Safe** | No (not required for Phase 1) |

### Test Cases

```python
# TC-get_all-01: Empty system
get_all_tasks()
→ Returns []

# TC-get_all-02: Single task
create_task("Task", "")
get_all_tasks()
→ Returns list with 1 task

# TC-get_all-03: Multiple tasks in order
create_task("First", "")
create_task("Second", "")
create_task("Third", "")
tasks = get_all_tasks()
→ tasks[0]["title"] == "First", tasks[1]["title"] == "Second", tasks[2]["title"] == "Third"

# TC-get_all-04: Includes all fields
tasks = get_all_tasks()
task = tasks[0]
→ task has keys: id, title, description, status

# TC-get_all-05: After deletion, gaps are visible
create_task("Task 1", "")  # id=1
create_task("Task 2", "")  # id=2
create_task("Task 3", "")  # id=3
delete_task(2)
tasks = get_all_tasks()
→ tasks[0]["id"] == 1, tasks[1]["id"] == 3 (no id 2)
```

---

## Function: `get_task_by_id`

### Signature

```python
def get_task_by_id(task_id: int) -> dict | None:
    """
    Retrieve a single task by its ID.

    Args:
        task_id: ID of the task to retrieve

    Returns:
        Task dict if found, None if not found

    Example:
        >>> get_task_by_id(1)
        {'id': 1, 'title': 'Task', 'description': '', 'status': 'Pending'}
        >>> get_task_by_id(999)
        None
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Lookup** | Linear search by id field; O(n) complexity |
| **Not Found** | Returns None (no error raised) |
| **Invalid Type** | Expects int; behavior for non-int is undefined |
| **Negative ID** | No tasks have ID < 1; returns None |
| **Side Effect** | None (read-only operation) |
| **Idempotent** | Yes (same input → same output) |

### Test Cases

```python
# TC-get_by_id-01: Found
create_task("Task", "Description")
task = get_task_by_id(1)
→ Returns task dict with id=1

# TC-get_by_id-02: Not found
get_task_by_id(999)
→ Returns None

# TC-get_by_id-03: After deletion
create_task("Task 1", "")
create_task("Task 2", "")
delete_task(1)
task = get_task_by_id(1)
→ Returns None (task no longer exists)

# TC-get_by_id-04: Correct task returned
create_task("Task 1", "Desc 1")
create_task("Task 2", "Desc 2")
task = get_task_by_id(2)
→ task["title"] == "Task 2", task["description"] == "Desc 2"
```

---

## Function: `update_task`

### Signature

```python
def update_task(task_id: int, title: str = None, description: str = None) -> bool:
    """
    Update the title and/or description of an existing task.

    Args:
        task_id: ID of the task to update
        title: New title (optional; if not provided, title is unchanged)
        description: New description (optional; if not provided, description is unchanged)

    Returns:
        True if task was updated, False if task not found

    Raises:
        ValueError: If title is provided but empty or whitespace-only

    Example:
        >>> create_task("Old Title", "Old Desc")
        >>> update_task(1, title="New Title")
        True
        >>> task = get_task_by_id(1)
        >>> task["title"]
        'New Title'
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Partial Update** | Can update title, description, or both independently |
| **ID Unchanged** | task_id is never modified |
| **Status Unchanged** | Status is NOT changed by update_task (use toggle for that) |
| **Validation** | If title is provided, it must be non-empty (same rules as create_task) |
| **Not Found** | Returns False; no error raised |
| **No-op Update** | If neither title nor description provided, returns True (no-op) |
| **Side Effect** | Modifies internal _tasks list if task found |
| **Idempotent** | Yes (calling twice with same args → same state) |

### Test Cases

```python
# TC-update-01: Update title only
create_task("Old Title", "Description")
result = update_task(1, title="New Title")
task = get_task_by_id(1)
→ result == True, task["title"] == "New Title", task["description"] == "Description"

# TC-update-02: Update description only
create_task("Title", "Old Desc")
result = update_task(1, description="New Desc")
task = get_task_by_id(1)
→ result == True, task["title"] == "Title", task["description"] == "New Desc"

# TC-update-03: Update both
create_task("Old Title", "Old Desc")
result = update_task(1, title="New Title", description="New Desc")
task = get_task_by_id(1)
→ result == True, task["title"] == "New Title", task["description"] == "New Desc"

# TC-update-04: Task not found
result = update_task(999, title="Anything")
→ result == False

# TC-update-05: Empty title rejected
create_task("Title", "Desc")
with pytest.raises(ValueError):
    update_task(1, title="")
→ ValueError raised, original title unchanged

# TC-update-06: Status unchanged
create_task("Title", "")
toggle_task_status(1)  # Set to Completed
update_task(1, title="New Title")
task = get_task_by_id(1)
→ task["status"] == "Completed" (unchanged by update)
```

---

## Function: `delete_task`

### Signature

```python
def delete_task(task_id: int) -> bool:
    """
    Delete a task by its ID.

    Args:
        task_id: ID of the task to delete

    Returns:
        True if task was deleted, False if task not found

    Example:
        >>> create_task("Task to Delete", "")
        >>> delete_task(1)
        True
        >>> get_task_by_id(1)
        None
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Removal** | Task is completely removed from internal list |
| **ID Not Reused** | Even if task 1 is deleted, next new task gets ID N+1 (not 1) |
| **Gap in IDs** | After deleting task 2 from [1,2,3], remaining [1,3] is valid |
| **Not Found** | Returns False; no error raised |
| **Side Effect** | Modifies internal _tasks list; increments counter unchanged |
| **Idempotent** | No (calling twice on same ID → first True, second False) |

### Test Cases

```python
# TC-delete-01: Delete existing task
create_task("Task", "")
result = delete_task(1)
→ result == True, get_task_by_id(1) returns None

# TC-delete-02: Delete non-existent task
result = delete_task(999)
→ result == False

# TC-delete-03: ID not reused
create_task("Task 1", "")  # id=1
delete_task(1)
create_task("Task 2", "")  # id=2, NOT id=1
→ New task gets id=2

# TC-delete-04: Gaps are ok
create_task("Task 1", "")  # id=1
create_task("Task 2", "")  # id=2
create_task("Task 3", "")  # id=3
delete_task(2)
tasks = get_all_tasks()
→ len(tasks) == 2, task IDs are [1, 3]

# TC-delete-05: Delete removes from all_tasks
create_task("Task", "")
delete_task(1)
tasks = get_all_tasks()
→ len(tasks) == 0
```

---

## Function: `toggle_task_status`

### Signature

```python
def toggle_task_status(task_id: int) -> bool:
    """
    Toggle a task's status between 'Pending' and 'Completed'.

    Args:
        task_id: ID of the task to toggle

    Returns:
        True if status was toggled, False if task not found

    Example:
        >>> create_task("Task", "")
        >>> toggle_task_status(1)
        True
        >>> task = get_task_by_id(1)
        >>> task["status"]
        'Completed'
        >>> toggle_task_status(1)
        True
        >>> task = get_task_by_id(1)
        >>> task["status"]
        'Pending'
    """
```

### Behavior

| Aspect | Detail |
|--------|--------|
| **Toggle Logic** | "Pending" → "Completed" or "Completed" → "Pending" |
| **No Partial Toggle** | Cannot set status to arbitrary value; must be one of the two |
| **Title/Description Unchanged** | Only status is modified |
| **Not Found** | Returns False; no error raised |
| **Side Effect** | Modifies internal _tasks list if task found |
| **Idempotent** | No (calling twice → original state, but second call returns status change) |

### Test Cases

```python
# TC-toggle-01: Pending to Completed
create_task("Task", "")  # Initial: Pending
result = toggle_task_status(1)
task = get_task_by_id(1)
→ result == True, task["status"] == "Completed"

# TC-toggle-02: Completed back to Pending
create_task("Task", "")
toggle_task_status(1)  # Now Completed
result = toggle_task_status(1)
task = get_task_by_id(1)
→ result == True, task["status"] == "Pending"

# TC-toggle-03: Task not found
result = toggle_task_status(999)
→ result == False

# TC-toggle-04: Other fields unchanged
create_task("Task Title", "Task Description")
original_task = get_task_by_id(1)
toggle_task_status(1)
updated_task = get_task_by_id(1)
→ updated_task["title"] == original_task["title"]
→ updated_task["description"] == original_task["description"]
→ updated_task["id"] == original_task["id"]
→ only status changed
```

---

## Module-Level State

### Global Variables

```python
_tasks: list = []  # Store all Task dicts
_next_id: int = 1  # Next available ID for new task
```

**Invariants**:
- `_tasks` contains all active Task dicts
- `_next_id` is always > 0 and increments monotonically
- All task IDs in `_tasks` are < `_next_id`
- No duplicates in `_tasks` (each ID appears at most once)

### Reset Function (For Testing)

```python
def _reset_state() -> None:
    """
    Reset module state to initial condition (for testing).

    Clears all tasks and resets ID counter.

    WARNING: Use only in unit tests!
    """
    global _tasks, _next_id
    _tasks = []
    _next_id = 1
```

---

## Error Handling Strategy

### Function Contracts

All functions follow these error handling rules:

1. **ValueError**: Raised for validation errors (e.g., empty title)
   - Function docstring specifies which cases raise ValueError
   - Always include descriptive message

2. **Return False**: Used to indicate "not found" or "operation failed"
   - No exception raised
   - Clean way to handle missing IDs

3. **No Silent Failures**: All errors are explicit
   - Either raise exception or return False
   - Never return None to indicate failure (use False instead)

### Example Error Handling in Tests

```python
# When ValueError is expected
with pytest.raises(ValueError, match="Title cannot be empty"):
    create_task("", "")

# When False is expected (not found)
result = delete_task(999)
assert result == False

# When True is expected (success)
result = create_task("Task", "")
assert result != False  # Could be dict or True
```

---

## Usage Examples

### Scenario 1: Complete CRUD Cycle

```python
# Create
task = create_task("Buy groceries", "Milk, bread")
task_id = task["id"]  # = 1

# Read
all_tasks = get_all_tasks()
assert len(all_tasks) == 1

# Update
success = update_task(task_id, description="Milk, bread, butter")
assert success == True

# Toggle
success = toggle_task_status(task_id)
assert success == True
task = get_task_by_id(task_id)
assert task["status"] == "Completed"

# Delete
success = delete_task(task_id)
assert success == True
task = get_task_by_id(task_id)
assert task is None
```

### Scenario 2: Error Handling

```python
# Invalid input
try:
    create_task("", "")  # Empty title
except ValueError as e:
    print(f"Error: {e}")  # "Title cannot be empty"

# Not found
result = delete_task(999)
if not result:
    print("Task not found")

# Partial update
update_task(1, title="New Title")  # description stays same
```

---

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `create_task` | O(1) | Append to list + increment counter |
| `get_all_tasks` | O(1) | Return reference to list |
| `get_task_by_id` | O(n) | Linear search; n = num tasks |
| `update_task` | O(n) | Linear search + update |
| `delete_task` | O(n) | Linear search + remove |
| `toggle_task_status` | O(n) | Linear search + update |

**Acceptable for Phase 1**: All operations complete in <1ms even for 100+ tasks.

**Future Optimization**: Use dict indexed by ID for O(1) lookups if needed in Phase 2.
