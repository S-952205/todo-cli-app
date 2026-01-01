# ADR-002: In-Memory Storage with Sequential Auto-Incrementing IDs

**Status**: Accepted
**Date**: 2025-12-31
**Feature**: 001-crud-tasks (Phase 1 In-Memory Todo CLI)
**Deciders**: Claude Code Agent, Architecture Planning Workflow

## Context

The Phase 1 In-Memory Todo CLI requires a data storage strategy that:

- Aligns with constitutional principle II: "Single-User In-Memory Architecture" (no persistence)
- Supports task lookups by ID for operations (Update, Delete, Toggle)
- Generates unique IDs for each task automatically
- Maintains data only during application runtime (data lost on exit)
- Performs well for anticipated scope (~100 tasks maximum)

The choice of storage structure and ID management strategy impacts:
- Performance characteristics (O(1) vs O(n) lookups)
- Code complexity (simple list vs indexed dictionary)
- User experience (predictable sequential IDs vs gaps/reuse)
- Future extensibility (can be refactored to database in Phase 2)

## Decision

**Use a Python list of dictionaries with a global auto-incrementing counter for ID management:**

### Storage Structure

```python
# engine.py (module-level state)
_tasks: List[Dict] = []           # List of Task dictionaries
_next_id: int = 1                 # Global counter for next available ID

# Task structure (stored in _tasks list)
{
    "id": int,                    # Unique identifier (auto-assigned, sequential)
    "title": str,                 # Non-empty task title
    "description": str,           # Optional task description
    "status": str                 # "Pending" or "Completed"
}
```

### ID Management Strategy

- **Initialization**: `_next_id = 1` (first task gets ID 1)
- **Assignment**: When creating a task, assign `id = _next_id`, then increment `_next_id += 1`
- **Reuse Policy**: IDs are **never reused**, even after deletion
  - If task with ID 2 is deleted, ID 2 is never assigned to a future task
  - Next new task still receives ID = current `_next_id` value
- **Result**: IDs are sequential (1, 2, 3, ...) but may have gaps after deletion
  - Example: Create 3 tasks (IDs 1, 2, 3), delete task 2 → remaining IDs are [1, 3], next new task gets ID 4

### Lookup Strategy

- **Lookup Method**: Linear search through _tasks list
- **Complexity**: O(n) for finding a task by ID
- **Acceptable for Phase 1**: With max ~100 tasks, lookup is microseconds (negligible)

## Consequences

### Positive

- **Simplicity**: Uses native Python data structures (list + dict)
  - No external database or persistence library needed
  - Easy to understand code; no complex indexing logic
  - Minimal setup and initialization

- **Alignment with Spec**: Matches user expectations from feature spec
  - Users expect IDs numbered 1, 2, 3, ... (sequential)
  - Non-reuse aligns with spec assumption: "ID 1 created → deleted → next ID is 2, not 1"
  - No confusion from ID reuse or renumbering

- **Predictability**: ID behavior is deterministic and consistent
  - Developer can reliably predict what ID a new task will receive
  - Debugging easier (ID history is predictable)
  - No edge cases from ID reuse conflicts

- **Fast Creation**: Adding a new task is O(1)
  - Just append to list and increment counter
  - No index reorganization or rebalancing needed

- **Flexible Future Migration**: Can be refactored to faster structure in Phase 2
  - Could switch to dict indexed by ID for O(1) lookups if needed
  - Could add persistent storage (SQLite, PostgreSQL) without changing engine API
  - Migration would be internal to engine.py; no impact on interface.py or main.py

### Negative

- **Linear Lookup**: Finding a task by ID is O(n)
  - Not optimal for large datasets (1000+ tasks)
  - Acceptable for Phase 1 scope (~100 tasks)
  - Would become bottleneck if data grows significantly

- **Memory Usage**: Keeping tasks in memory uses RAM
  - ~500 bytes per task (id, title, description, status)
  - 100 tasks ≈ 50KB (negligible)
  - Data lost on application exit (acceptable per spec)

- **ID Gaps**: Deleted tasks leave gaps in ID sequence
  - If tasks 1, 2, 3 exist and task 2 is deleted, list shows [1, 3]
  - Might confuse users expecting sequential numbering with no gaps
  - Acceptable per assumptions; documented in spec

- **No Reuse**: IDs increment indefinitely
  - Counter never resets (could theoretically overflow in year 300+ with continuous operation)
  - Not a practical concern for Phase 1 (single-session, in-memory)

## Alternatives Considered

### Alternative 1: Dictionary Indexed by ID

**Structure**: Store tasks in dict with ID as key for O(1) lookup

```python
_tasks: Dict[int, Dict] = {}  # {1: {...}, 2: {...}, 3: {...}}
_next_id: int = 1
```

**Pros**:
- O(1) lookup by ID (faster for large datasets)
- Same sequential ID generation
- Can iterate values() to get all tasks

**Cons**:
- Slightly more complex (managing dict vs list)
- Requires iteration of dict.values() for "get all tasks" (same O(n) as list iteration)
- Dict ordering guarantees (Python 3.7+) work, but list is more explicit about insertion order
- Minimal benefit for Phase 1 scope (100 tasks)

**Rejected because**: Premature optimization for Phase 1 scope; added complexity not justified; can refactor in Phase 2 if needed

### Alternative 2: Reuse Deleted IDs

**Structure**: Track deleted IDs and reuse them for new tasks

```python
_tasks: List[Dict] = []
_next_id: int = 1
_deleted_ids: Set[int] = set()  # Track reusable IDs

# On delete: _deleted_ids.add(task_id)
# On create: reuse from _deleted_ids if available, else use _next_id
```

**Pros**:
- Prevents ID counter from growing indefinitely
- Could keep ID range smaller (1-N vs 1-1000+)
- Potentially more "natural" (no gaps)

**Cons**:
- More complex bookkeeping (tracking deleted IDs)
- Unpredictable ID assignment (user can't predict what ID they'll get)
- Multiple ways to achieve same outcome → confusing for developers
- Harder to debug ("Why did my task get ID 5 instead of 4?")
- Violates assumption in spec: "IDs remain sequential even if deleted"

**Rejected because**: Adds complexity without benefit; violates spec expectations; makes behavior unpredictable

### Alternative 3: UUID or Unique String IDs

**Structure**: Use UUID or hash-based identifiers instead of sequential integers

```python
import uuid
_tasks: Dict[str, Dict] = {}  # {"uuid-1234": {...}, "uuid-5678": {...}}
```

**Pros**:
- Globally unique (no reuse issues)
- No counter management needed
- Suitable for distributed systems

**Cons**:
- More complex for users (IDs are long strings like "550e8400-e29b-41d4-a716-446655440000")
- Violates spec expectation of simple numeric IDs (1, 2, 3)
- Harder for users to remember or reference tasks
- Overkill for single-user, single-session application

**Rejected because**: Violates spec; too complex for Phase 1; doesn't fit single-user CLI model

### Alternative 4: Database (SQLite/PostgreSQL)

**Structure**: Use persistent database with auto-increment primary keys

```python
# database: CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, ...)
import sqlite3
conn = sqlite3.connect("tasks.db")
```

**Pros**:
- Data persists across sessions
- Proven scalable solution
- Supports future multi-user features
- Built-in ID management

**Cons**:
- Violates constitutional principle II: "In-Memory Architecture" (no persistence for Phase 1)
- Adds complexity (database setup, migrations, connection management)
- Unnecessary for Phase 1 single-session requirement
- Defeats purpose of in-memory-only design

**Rejected because**: Violates Phase 1 in-memory-only constraint; over-engineered; spec explicitly rejects persistence

## Implementation Approach

### Engine Module Structure

```python
# src/engine.py

_tasks: List[Dict] = []
_next_id: int = 1

def create_task(title: str, description: str = "") -> Dict:
    """Create task with auto-assigned ID."""
    global _next_id
    task = {
        "id": _next_id,
        "title": title.strip(),
        "description": description.strip(),
        "status": "Pending"
    }
    _tasks.append(task)
    _next_id += 1
    return task

def get_task_by_id(task_id: int) -> Optional[Dict]:
    """Find task by ID (linear search)."""
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None

def _reset_state():
    """Reset to initial state (testing only)."""
    global _tasks, _next_id
    _tasks = []
    _next_id = 1
```

### Testing Strategy

- **Unit Tests**: Verify ID assignment, sequential generation, non-reuse
- **Integration Tests**: Verify storage persists across multiple operations
- **Edge Case Tests**: Test with 0 tasks, 1 task, 100 tasks
- **No Persistence Tests**: Verify data is lost on module reload (expected)

## References

- **Plan**: `specs/001-crud-tasks/plan.md` - Section "Key Architectural Decisions #1, 2"
- **Data Model**: `specs/001-crud-tasks/data-model.md` - "Storage Model" and "ID Management" sections
- **Contracts**: `specs/001-crud-tasks/contracts/engine_contracts.md` - Function specifications with O(n) complexity noted
- **Spec**: `specs/001-crud-tasks/spec.md` - Assumptions section (ID assignment and in-memory-only constraint)
- **Constitution**: `.specify/memory/constitution.md` - Principle II (Single-User In-Memory Architecture)

## Phase 2+ Considerations

**If scaling becomes necessary in Phase 2:**

1. **Optimize Lookup**: Switch to dict[id] for O(1) access
   - Internal refactor; no impact on engine.py public API
   - Tests remain unchanged (same contracts)

2. **Add Persistence**: Introduce SQLite or PostgreSQL
   - Requires constitutional amendment (violates "in-memory only")
   - Would need migration strategy for existing data
   - Recommendation: Create new Phase 2 feature for persistence

3. **Multi-User Support**: Transition from single-session to multi-user
   - Requires constitutional amendment
   - Would add user_id field to tasks
   - Would need database for cross-session state

All Phase 2+ changes can be made inside engine.py without affecting interface.py or main.py (sealed abstraction).

## Rollback Plan

If performance issues arise during Phase 1:

1. **Test with real data**: Load 100+ tasks and measure lookup time
2. **Profile bottlenecks**: Use Python cProfile to identify actual slowdowns
3. **If needed**: Refactor to dict[id] structure (5-10 minute change)
4. **Backward compatible**: Public API contracts unchanged

Expected outcome: No refactoring needed for Phase 1 scope.
