"""
Business logic for task management (CRUD operations).

This module implements all core task operations independent of the CLI interface.
Tasks are stored in-memory in a Python list; data is lost on application exit.
"""

from typing import Optional

from src.models import validate_description, validate_title

# In-memory storage
_tasks = []  # List of task dicts
_next_id = 1  # Global counter for auto-incrementing IDs


def create_task(title: str, description: str = "") -> dict:
    """
    Create a new task with auto-assigned ID and "Pending" status.

    Args:
        title: Non-empty task title (whitespace will be stripped)
        description: Optional task description; defaults to empty string

    Returns:
        Task dict with keys: id, title, description, status

    Raises:
        ValueError: If title is empty or only whitespace

    Example:
        >>> task = create_task("Buy milk", "From the store")
        >>> task["id"]
        1
        >>> task["status"]
        'Pending'
    """
    global _next_id

    # Validate title (will raise ValueError if invalid)
    validate_title(title)

    # Create task with auto-assigned ID
    task = {
        "id": _next_id,
        "title": title.strip(),
        "description": validate_description(description),
        "status": "Pending",
    }

    # Store task and increment counter
    _tasks.append(task)
    _next_id += 1

    return task


def get_all_tasks() -> list:
    """
    Retrieve all tasks from the system.

    Returns:
        List of task dicts in creation order (earliest first)
        Empty list if no tasks exist

    Example:
        >>> get_all_tasks()
        [{'id': 1, 'title': 'Task 1', ...}, {'id': 2, 'title': 'Task 2', ...}]
    """
    return _tasks.copy()


def get_task_by_id(task_id: int) -> Optional[dict]:
    """
    Retrieve a single task by its ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        Task dict if found, None if not found

    Example:
        >>> get_task_by_id(1)
        {'id': 1, 'title': 'Task', 'description': '', 'status': 'Pending'}
        >>> get_task_by_id(999)
        None
    """
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(task_id: int, title: str = None, description: str = None) -> bool:
    """
    Update the title and/or description of an existing task.

    Args:
        task_id: ID of the task to update
        title: New title (optional; if provided must be non-empty)
        description: New description (optional; can be empty)

    Returns:
        True if task was updated, False if task not found

    Raises:
        ValueError: If title is provided but is empty

    Note:
        Status is NOT changed by this function; use toggle_task_status for that.

    Example:
        >>> create_task("Old Title", "Old Desc")
        >>> update_task(1, title="New Title")
        True
        >>> update_task(999, title="Anything")
        False
    """
    # Find task by ID
    for task in _tasks:
        if task["id"] == task_id:
            # Validate and update title if provided
            if title is not None:
                validate_title(title)  # Will raise ValueError if invalid
                task["title"] = title.strip()

            # Validate and update description if provided
            if description is not None:
                task["description"] = validate_description(description)

            return True

    # Task not found
    return False


def delete_task(task_id: int) -> bool:
    """
    Delete a task by its ID.

    Args:
        task_id: ID of the task to delete

    Returns:
        True if task was deleted, False if task not found

    Note:
        Deleted task IDs are not reused; next new task still gets _next_id.

    Example:
        >>> create_task("Task", "")
        >>> delete_task(1)
        True
        >>> get_task_by_id(1)
        None
    """
    for i, task in enumerate(_tasks):
        if task["id"] == task_id:
            _tasks.pop(i)
            return True
    return False


def toggle_task_status(task_id: int) -> bool:
    """
    Toggle a task's status between "Pending" and "Completed".

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
    """
    for task in _tasks:
        if task["id"] == task_id:
            # Toggle between Pending and Completed
            task["status"] = "Pending" if task["status"] == "Completed" else "Completed"
            return True
    return False


def _get_task_index(task_id: int) -> int:
    """
    Helper: Find the index of a task in the _tasks list by ID.

    Args:
        task_id: The task ID to search for

    Returns:
        Index in _tasks list, or -1 if not found

    Note:
        This is an internal helper function for engine operations.
    """
    for i, task in enumerate(_tasks):
        if task["id"] == task_id:
            return i
    return -1


def _reset_state() -> None:
    """
    Reset module state to initial condition.

    Clears all tasks and resets the ID counter to 1.

    Warning:
        Use only in unit tests or when you need to start fresh!
    """
    global _tasks, _next_id
    _tasks = []
    _next_id = 1
