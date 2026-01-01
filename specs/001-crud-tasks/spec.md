# Feature Specification: Phase 1 In-Memory Todo CLI

**Feature Branch**: `001-crud-tasks`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase 1 In-Memory Todo CLI - Focus: Core Task Management (CRUD) - Target: Terminal-based interactive application"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

A user needs to create a new task with a title and description. The system should assign a unique ID automatically and set the initial status to "Pending". This is the foundation of the todo app.

**Why this priority**: P1 - Creating tasks is the most fundamental operation; without this, users cannot populate the todo list.

**Independent Test**: Can be fully tested by launching app, selecting "Add Task", entering title and description, and verifying the task appears in the list with a unique ID and "Pending" status.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** user selects "Add Task" and enters title "Buy groceries" and description "Milk, bread, eggs", **Then** a new task is created with a unique ID, title "Buy groceries", description "Milk, bread, eggs", and status "Pending"
2. **Given** a task exists with ID 1, **When** user creates a new task, **Then** the new task receives a unique ID (2 or higher) that does not duplicate any existing task ID

---

### User Story 2 - View All Tasks (Priority: P1)

A user needs to see all tasks in a formatted list. The display must show task ID, title, status indicator, and description for easy scanning.

**Why this priority**: P1 - Without a clear view of all tasks, users cannot effectively manage their todo list.

**Independent Test**: Can be fully tested by adding tasks and selecting "View Tasks", verifying all tasks appear in a formatted list with ID, title, status `[ ]` for pending or `[X]` for completed, and description.

**Acceptance Scenarios**:

1. **Given** three tasks exist in the system, **When** user selects "View Tasks", **Then** all three tasks are displayed in a formatted list with each task showing ID, title, status indicator, and description
2. **Given** an empty task list, **When** user selects "View Tasks", **Then** a message indicates no tasks exist
3. **Given** tasks exist, **When** user views the list, **Then** pending tasks show `[ ]` status indicator and completed tasks show `[X]` status indicator

---

### User Story 3 - Update Task (Priority: P2)

A user needs to modify the title or description of an existing task by its ID. The system must validate the ID exists before allowing modification.

**Why this priority**: P2 - Allows users to correct or refine task details after creation; essential for practical task management but less critical than viewing tasks.

**Independent Test**: Can be fully tested by creating a task, selecting "Update Task", providing ID and new title/description, and verifying changes appear in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with title "Buy groceries", **When** user updates ID 1 with new title "Buy groceries and cook dinner", **Then** the task title is changed and other fields remain unchanged
2. **Given** a task with ID 2 exists, **When** user updates ID 2 with a new description, **Then** only the description is updated, title and ID remain unchanged
3. **Given** user attempts to update task with ID 999, **When** the ID does not exist, **Then** system displays an error message indicating the task ID was not found

---

### User Story 4 - Delete Task (Priority: P2)

A user needs to remove a task from the list by its ID. The system must confirm the ID exists before deletion.

**Why this priority**: P2 - Allows cleanup of completed or unwanted tasks; important for keeping lists manageable but can be achieved after core features are working.

**Independent Test**: Can be fully tested by creating a task, selecting "Delete Task", providing the task ID, and verifying the task no longer appears in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** user deletes task ID 1, **Then** the task is removed and no longer appears in "View Tasks"
2. **Given** user attempts to delete task with ID 999, **When** the ID does not exist, **Then** system displays an error message indicating the task ID was not found
3. **Given** five tasks exist (IDs 1-5), **When** user deletes task ID 3, **Then** tasks 1, 2, 4, 5 remain and task 3 is gone

---

### User Story 5 - Toggle Task Status (Priority: P2)

A user needs to mark a task as completed or revert it back to pending by toggling its status. This provides visual feedback of progress.

**Why this priority**: P2 - Core for tracking completion progress; completes the basic CRUD set but less critical than initial creation and viewing.

**Independent Test**: Can be fully tested by creating a task with "Pending" status, toggling it to "Completed" (displaying as `[X]`), toggling back to "Pending" (displaying as `[ ]`).

**Acceptance Scenarios**:

1. **Given** a task has status "Pending" (shown as `[ ]`), **When** user toggles task status, **Then** the status changes to "Completed" (shown as `[X]`)
2. **Given** a task has status "Completed" (shown as `[X]`), **When** user toggles task status, **Then** the status changes to "Pending" (shown as `[ ]`)
3. **Given** user toggles status of task ID 5, **When** that ID does not exist, **Then** system displays an error message indicating the task ID was not found

---

### Edge Cases

- What happens when user enters a non-numeric ID for operations that require an ID (Update, Delete, Toggle)? System should reject with a clear error message.
- What happens when user enters extremely long title or description? System should accept and store the full text (no artificial length limits for Phase 1).
- What happens when user attempts to add a task with an empty title? System should either reject or require a title before accepting.
- What happens when user exits the app? All data is lost (in-memory only) - this is expected Phase 1 behavior.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a new task with a title and description
- **FR-002**: System MUST automatically assign a unique ID to each new task
- **FR-003**: System MUST initialize each new task with status "Pending"
- **FR-004**: System MUST display all tasks in a formatted list showing ID, title, status indicator, and description
- **FR-005**: System MUST allow users to update the title and/or description of an existing task by ID
- **FR-006**: System MUST allow users to delete a task by ID
- **FR-007**: System MUST allow users to toggle a task's status between "Pending" and "Completed"
- **FR-008**: System MUST display status as `[ ]` for Pending tasks and `[X]` for Completed tasks
- **FR-009**: System MUST reject operations (Update, Delete, Toggle) on non-existent task IDs with a clear error message
- **FR-010**: System MUST reject non-numeric ID inputs with a clear error message
- **FR-011**: System MUST provide an interactive menu allowing users to select operations (Add, View, Update, Delete, Toggle, Exit)
- **FR-012**: System MUST handle invalid menu selections gracefully without crashing

### Key Entities

- **Task**: Represents a single todo item. Key attributes:
  - `id` (integer, unique, auto-assigned): Unique identifier for the task
  - `title` (string): User-provided task title
  - `description` (string): User-provided task description or details
  - `status` (string, enum: "Pending" or "Completed"): Current state of the task

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, view, update, delete, and toggle tasks without the application crashing on valid inputs
- **SC-002**: All invalid inputs (non-numeric IDs, non-existent IDs, invalid menu selections) are handled gracefully with clear user-friendly error messages
- **SC-003**: Task data remains consistent in memory throughout the session (IDs are unique, status changes persist until toggled again)
- **SC-004**: The interactive menu is intuitive; users can understand all available operations without documentation
- **SC-005**: Code adheres to PEP 8 style guide with no formatting violations
- **SC-006**: Business logic (Task model and operations) is completely separated from CLI display logic
- **SC-007**: All functions and classes have comprehensive docstrings explaining purpose, parameters, and return values
- **SC-008**: All operations complete within 1 second (no performance degradation with in-memory operations)

## Assumptions

- The app runs as a single-user, single-session process; persistence (saving to files/database) is explicitly out of scope for Phase 1
- Task IDs are assigned sequentially starting from 1 and increment by 1 for each new task
- Invalid user inputs (non-numeric IDs, out-of-range menus, etc.) should be reported in plain English error messages, not technical stack traces
- Menu selection is case-insensitive (e.g., both "add" and "ADD" are accepted) or uses numbered options
- A task must have a non-empty title; description can be empty (reasonable default for optional descriptions)
- The terminal environment supports basic text output and keyboard input (no GUI)

## Out of Scope (Phase 1)

- Persistence to files or databases
- Multi-user support
- Cloud synchronization
- Rich text formatting
- Task categories, tags, or priorities
- Recurring tasks
- Due dates or reminders
- Undo/redo functionality
- Task filtering or sorting
- Collaborative editing
- Search functionality

## Next Steps

Once this specification is approved, proceed to `/sp.plan` to design the architecture and module structure for implementation.
