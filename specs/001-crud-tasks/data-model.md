# Data Model: Phase 1 In-Memory Todo CLI

**Created**: 2025-12-31
**Feature**: 001-crud-tasks
**Purpose**: Define entities, relationships, and validation rules for in-memory task storage

## Core Entity: Task

### Structure

```python
Task = {
    "id": int,              # Unique identifier
    "title": str,           # Task title/summary
    "description": str,     # Task details
    "status": str           # Current state: "Pending" or "Completed"
}
```

### Field Definitions

| Field | Type | Required | Auto-Assigned | Constraints | Example |
|-------|------|----------|---|---|---|
| `id` | int | Yes | Yes (auto-increment) | Unique, >= 1, sequential | 1, 2, 3, ... |
| `title` | str | Yes | No | Non-empty, max length = Python str limit | "Buy groceries" |
| `description` | str | No | No | Can be empty, max length = Python str limit | "Milk, bread, eggs" |
| `status` | str | Yes | Yes (default="Pending") | Enum: "Pending" \| "Completed" | "Pending" or "Completed" |

### Validation Rules

1. **ID Validation**
   - Must be an integer
   - Must be >= 1
   - Must be unique across all tasks
   - Assigned automatically (user cannot set)
   - Never reused after deletion

2. **Title Validation**
   - Must be a non-empty string
   - Cannot contain only whitespace
   - User input is stripped of leading/trailing whitespace
   - No maximum length limit for Phase 1

3. **Description Validation**
   - Must be a string
   - Can be empty (optional field)
   - User input is stripped of leading/trailing whitespace
   - No maximum length limit for Phase 1

4. **Status Validation**
   - Must be exactly "Pending" or "Completed"
   - Case-sensitive (only these exact values)
   - Assigned automatically on creation (default: "Pending")
   - Cannot be set to other values

### State Transitions

```
       create_task
           |
           v
    ┌──────────────┐
    │    Task      │
    │  "Pending"   │
    └──────────────┘
           ^
           |
    toggle_status
           |
           v
    ┌──────────────┐
    │    Task      │
    │ "Completed"  │
    └──────────────┘
```

**Creation**: All new tasks start in "Pending" state
**Toggle**: User can flip between "Pending" ↔ "Completed" via toggle_task_status()
**Update**: Title and description can be modified independently; status is NOT changed by update_task()
**Deletion**: Task is removed from system entirely via delete_task()

## Storage Model

### In-Memory List

Tasks are stored in a module-level list:

```python
# engine.py (pseudo-code)
_tasks = []  # List[Dict] - stores Task dicts in creation order
_next_id = 1  # Module-level counter for auto-incrementing IDs
```

### Key Characteristics

- **Structure**: Python list of dictionaries (simple, lightweight)
- **Order**: Tasks are stored in creation order (insertion order)
- **Lookup**: Linear search by ID (O(n)) - acceptable for Phase 1 scope
- **Persistence**: None (data lost on application exit) - expected behavior
- **Thread Safety**: Not required (single-user, single-threaded application)

### Example In-Memory State

```python
_tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, bread, eggs",
        "status": "Pending"
    },
    {
        "id": 2,
        "title": "Review pull requests",
        "description": "",
        "status": "Completed"
    },
    {
        "id": 3,
        "title": "Prepare presentation",
        "description": "Q4 results for board meeting",
        "status": "Pending"
    }
]
_next_id = 4  # Next task will get ID 4
```

## ID Management

### Auto-Incrementing Counter Pattern

```python
_next_id = 1  # Initialize to 1 (first task ID is 1)

def create_task(title: str, description: str) -> Task:
    global _next_id
    task_id = _next_id
    _next_id += 1  # Increment for next task
    # ... create task with this task_id
```

### Behavior

- **Initial ID**: First task created receives ID = 1
- **Sequential**: Each subsequent task increments by 1 (1, 2, 3, 4, ...)
- **No Reuse**: Even if task ID 2 is deleted, ID 2 is never reused
- **Gaps Allowed**: If task 1 and 3 exist (2 deleted), that's valid; display shows 1, 3
- **Never Wraps**: IDs only increase; no modulo arithmetic or wrapping

### Justification

This simple auto-increment approach:
- Is trivial to implement (one counter variable)
- Matches user expectations (tasks numbered 1, 2, 3, ...)
- Avoids complexity of reusing deleted IDs
- Makes IDs predictable for the user

## Relationships

### Between Tasks

**No relationships defined for Phase 1**. Each task is independent:
- No parent-child relationships
- No task dependencies
- No linking between tasks
- No ordering or categorization

Future phases may add:
- Task categories or tags (Phase 2)
- Subtasks or dependencies (Phase 3)
- Shared tasks or mentions (later phases)

## Constraints & Invariants

### Invariants (Must Always Be True)

1. Every task has a unique ID
2. No two tasks share the same ID
3. All task IDs are >= 1
4. Every task has a non-empty title
5. Every task status is either "Pending" or "Completed"
6. Tasks cannot have null/None for id, title, or status
7. New tasks always start with status "Pending"

### Constraints

1. **Storage Constraint**: In-memory only; no persistence to disk
2. **Scope Constraint**: Only 5 fields per task (id, title, description, status) - no extras for Phase 1
3. **User Constraint**: Single user; no multi-user coordination
4. **Session Constraint**: Data exists only during application runtime

## Example Operations & State Changes

### Operation 1: Create Two Tasks

```
Initial: _tasks = [], _next_id = 1

create_task("Buy groceries", "Milk, bread")
  _tasks = [{"id": 1, "title": "Buy groceries", "description": "Milk, bread", "status": "Pending"}]
  _next_id = 2

create_task("Exercise", "")
  _tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, bread", "status": "Pending"},
    {"id": 2, "title": "Exercise", "description": "", "status": "Pending"}
  ]
  _next_id = 3
```

### Operation 2: Toggle Task 1 Status

```
Before: Task 1 = {"id": 1, "title": "Buy groceries", ..., "status": "Pending"}

toggle_task_status(1)
  Task 1 = {"id": 1, "title": "Buy groceries", ..., "status": "Completed"}

After: Task 1 is now "Completed"
```

### Operation 3: Update Task 1 Description

```
Before: Task 1 = {"id": 1, "title": "Buy groceries", "description": "Milk, bread", "status": "Completed"}

update_task(1, description="Milk, bread, butter, cheese")
  Task 1 = {"id": 1, "title": "Buy groceries", "description": "Milk, bread, butter, cheese", "status": "Completed"}

After: Description updated; title and status unchanged
```

### Operation 4: Delete Task 2

```
Before:
  _tasks = [
    {"id": 1, ...},
    {"id": 2, "title": "Exercise", ...},
    {"id": 3, ...}
  ]

delete_task(2)
  _tasks = [
    {"id": 1, ...},
    {"id": 3, ...}
  ]

After: Task 2 is removed; Task 3 still exists with ID 3 (IDs not renumbered)
```

## Edge Cases & Boundary Conditions

### Edge Case 1: Empty List
- **Condition**: User selects "View Tasks" when no tasks exist
- **Expected Behavior**: Display message "No tasks exist" or "Your task list is empty"
- **Data State**: _tasks = [], _next_id = 1

### Edge Case 2: Non-Empty Title with Empty Description
- **Condition**: User creates task with title only
- **Expected Behavior**: Task created successfully with description = ""
- **Data State**: Task exists with empty description field

### Edge Case 3: Delete All Tasks
- **Condition**: User deletes all tasks one by one
- **Expected Behavior**: _tasks becomes empty; _next_id continues incrementing
- **Data State**: _tasks = [], _next_id = N (where N > 1)

### Edge Case 4: Very Long Title/Description
- **Condition**: User enters extremely long string (1000+ characters)
- **Expected Behavior**: Accept and store the full string (Python str has no artificial limit)
- **Data State**: Task exists with full long text in title/description

### Edge Case 5: Whitespace-Only Input
- **Condition**: User enters only spaces for title: "    "
- **Expected Behavior**: Reject as empty (after stripping, becomes "")
- **Data State**: Task not created; user is re-prompted

## Testing Implications

### Unit Tests Should Verify:

1. **ID Assignment**: Auto-incrementing IDs are unique and sequential
2. **Validation**: Empty titles are rejected; descriptions can be empty
3. **State Transitions**: Status toggles correctly between "Pending" and "Completed"
4. **CRUD Operations**: Create, Read, Update, Delete all modify state correctly
5. **Edge Cases**: Empty list, long strings, whitespace handling

### Integration Tests Should Verify:

1. **Full Workflow**: Add → View → Update → Toggle → Delete
2. **ID Persistence**: IDs don't change after updates or other operations
3. **Error Handling**: Invalid IDs return appropriate error messages
4. **Data Consistency**: State remains valid after multiple operations

## Future Schema Evolution (Phase 2+)

Current model is intentionally minimal. Future enhancements may include:

- **Categories/Tags**: Add `category: str` or `tags: List[str]`
- **Timestamps**: Add `created_at` and `updated_at` timestamps
- **Priority**: Add `priority: str` (Low/Medium/High)
- **Due Date**: Add `due_date: str` (ISO date)
- **Attachments**: Add `attachments: List[str]` (file paths or URLs)
- **Subtasks**: Add nested structure with parent-child relationships

These additions will require amendments to the constitution (new scope) before implementation.
