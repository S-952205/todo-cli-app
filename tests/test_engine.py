"""
Unit tests for the engine module (business logic).

Tests all CRUD operations and edge cases.
"""

import pytest
from src import engine


@pytest.fixture(autouse=True)
def reset_engine():
    """Reset engine state before each test."""
    engine._reset_state()
    yield
    engine._reset_state()


# ============================================================================
# Tests for create_task
# ============================================================================


def test_create_task_basic():
    """Verify basic task creation with title and description."""
    task = engine.create_task("Buy milk", "From the store")

    assert task["id"] == 1
    assert task["title"] == "Buy milk"
    assert task["description"] == "From the store"
    assert task["status"] == "Pending"


def test_create_task_id_uniqueness():
    """Verify that IDs are unique and sequential."""
    task1 = engine.create_task("Task 1", "")
    task2 = engine.create_task("Task 2", "")
    task3 = engine.create_task("Task 3", "")

    assert task1["id"] == 1
    assert task2["id"] == 2
    assert task3["id"] == 3
    assert task1["id"] != task2["id"]
    assert task2["id"] != task3["id"]


def test_create_task_empty_title_rejected():
    """Verify that empty titles are rejected."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        engine.create_task("", "Description")


def test_create_task_whitespace_title_rejected():
    """Verify that whitespace-only titles are rejected."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        engine.create_task("   ", "Description")


def test_create_task_title_stripped():
    """Verify that title whitespace is stripped."""
    task = engine.create_task("  Task Title  ", "")
    assert task["title"] == "Task Title"


def test_create_task_empty_description_allowed():
    """Verify that empty descriptions are allowed."""
    task = engine.create_task("Task", "")
    assert task["description"] == ""


def test_create_task_description_stripped():
    """Verify that description whitespace is stripped."""
    task = engine.create_task("Task", "  Description  ")
    assert task["description"] == "Description"


def test_create_task_default_status_pending():
    """Verify that new tasks have 'Pending' status."""
    task = engine.create_task("Task", "")
    assert task["status"] == "Pending"


# ============================================================================
# Tests for get_all_tasks
# ============================================================================


def test_get_all_tasks_empty():
    """Verify get_all_tasks returns empty list when no tasks exist."""
    tasks = engine.get_all_tasks()
    assert tasks == []


def test_get_all_tasks_single():
    """Verify get_all_tasks returns list with single task."""
    engine.create_task("Task", "")
    tasks = engine.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task"


def test_get_all_tasks_multiple():
    """Verify get_all_tasks returns all tasks in order."""
    engine.create_task("First", "")
    engine.create_task("Second", "")
    engine.create_task("Third", "")

    tasks = engine.get_all_tasks()
    assert len(tasks) == 3
    assert tasks[0]["title"] == "First"
    assert tasks[1]["title"] == "Second"
    assert tasks[2]["title"] == "Third"


def test_get_all_tasks_creation_order():
    """Verify that tasks are returned in creation order."""
    task1 = engine.create_task("Task 1", "")
    task2 = engine.create_task("Task 2", "")
    task3 = engine.create_task("Task 3", "")

    tasks = engine.get_all_tasks()
    assert tasks[0]["id"] == task1["id"]
    assert tasks[1]["id"] == task2["id"]
    assert tasks[2]["id"] == task3["id"]


# ============================================================================
# Tests for get_task_by_id
# ============================================================================


def test_get_task_by_id_found():
    """Verify get_task_by_id returns task when found."""
    engine.create_task("Task", "Description")
    task = engine.get_task_by_id(1)

    assert task is not None
    assert task["id"] == 1
    assert task["title"] == "Task"
    assert task["description"] == "Description"


def test_get_task_by_id_not_found():
    """Verify get_task_by_id returns None when task not found."""
    task = engine.get_task_by_id(999)
    assert task is None


def test_get_task_by_id_correct_task():
    """Verify get_task_by_id returns correct task when multiple exist."""
    engine.create_task("Task 1", "")
    engine.create_task("Task 2", "")
    engine.create_task("Task 3", "")

    task = engine.get_task_by_id(2)
    assert task["title"] == "Task 2"
    assert task["id"] == 2


# ============================================================================
# Tests for update_task
# ============================================================================


def test_update_task_title():
    """Verify update_task can update task title."""
    engine.create_task("Old Title", "Description")
    success = engine.update_task(1, title="New Title")

    assert success is True
    task = engine.get_task_by_id(1)
    assert task["title"] == "New Title"
    assert task["description"] == "Description"


def test_update_task_description():
    """Verify update_task can update task description."""
    engine.create_task("Title", "Old Description")
    success = engine.update_task(1, description="New Description")

    assert success is True
    task = engine.get_task_by_id(1)
    assert task["title"] == "Title"
    assert task["description"] == "New Description"


def test_update_task_both():
    """Verify update_task can update both title and description."""
    engine.create_task("Old Title", "Old Description")
    success = engine.update_task(1, title="New Title", description="New Description")

    assert success is True
    task = engine.get_task_by_id(1)
    assert task["title"] == "New Title"
    assert task["description"] == "New Description"


def test_update_task_not_found():
    """Verify update_task returns False when task not found."""
    success = engine.update_task(999, title="Anything")
    assert success is False


def test_update_task_empty_title_rejected():
    """Verify update_task rejects empty title."""
    engine.create_task("Title", "")

    with pytest.raises(ValueError, match="Title cannot be empty"):
        engine.update_task(1, title="")


def test_update_task_status_unchanged():
    """Verify that update_task does not change task status."""
    engine.create_task("Title", "")
    engine.toggle_task_status(1)  # Change to Completed

    engine.update_task(1, title="New Title")
    task = engine.get_task_by_id(1)
    assert task["status"] == "Completed"


# ============================================================================
# Tests for delete_task
# ============================================================================


def test_delete_task_success():
    """Verify delete_task removes task."""
    engine.create_task("Task", "")
    success = engine.delete_task(1)

    assert success is True
    assert engine.get_task_by_id(1) is None
    assert engine.get_all_tasks() == []


def test_delete_task_not_found():
    """Verify delete_task returns False when task not found."""
    success = engine.delete_task(999)
    assert success is False


def test_delete_task_id_not_reused():
    """Verify that deleted task IDs are not reused."""
    engine.create_task("Task 1", "")
    engine.delete_task(1)
    task2 = engine.create_task("Task 2", "")

    assert task2["id"] == 2  # Not 1


def test_delete_task_removes_from_list():
    """Verify that delete_task actually removes task from list."""
    engine.create_task("Task 1", "")
    engine.create_task("Task 2", "")
    engine.create_task("Task 3", "")

    engine.delete_task(2)
    tasks = engine.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 3


def test_delete_task_with_gaps():
    """Verify that remaining tasks are accessible after deletion."""
    engine.create_task("Task 1", "")
    engine.create_task("Task 2", "")
    engine.create_task("Task 3", "")

    engine.delete_task(2)

    task1 = engine.get_task_by_id(1)
    task3 = engine.get_task_by_id(3)

    assert task1 is not None
    assert task3 is not None


# ============================================================================
# Tests for toggle_task_status
# ============================================================================


def test_toggle_task_status_pending_to_completed():
    """Verify toggle changes Pending to Completed."""
    engine.create_task("Task", "")
    success = engine.toggle_task_status(1)

    assert success is True
    task = engine.get_task_by_id(1)
    assert task["status"] == "Completed"


def test_toggle_task_status_completed_to_pending():
    """Verify toggle changes Completed back to Pending."""
    engine.create_task("Task", "")
    engine.toggle_task_status(1)  # Now Completed
    success = engine.toggle_task_status(1)  # Toggle back

    assert success is True
    task = engine.get_task_by_id(1)
    assert task["status"] == "Pending"


def test_toggle_task_status_not_found():
    """Verify toggle returns False when task not found."""
    success = engine.toggle_task_status(999)
    assert success is False


def test_toggle_task_status_other_fields_unchanged():
    """Verify toggle does not affect other fields."""
    engine.create_task("Task Title", "Task Description")
    engine.toggle_task_status(1)

    task = engine.get_task_by_id(1)
    assert task["title"] == "Task Title"
    assert task["description"] == "Task Description"
    assert task["id"] == 1


def test_toggle_task_status_multiple_times():
    """Verify toggle can be called multiple times."""
    engine.create_task("Task", "")

    engine.toggle_task_status(1)
    task = engine.get_task_by_id(1)
    assert task["status"] == "Completed"

    engine.toggle_task_status(1)
    task = engine.get_task_by_id(1)
    assert task["status"] == "Pending"

    engine.toggle_task_status(1)
    task = engine.get_task_by_id(1)
    assert task["status"] == "Completed"


# ============================================================================
# Integration tests
# ============================================================================


def test_complete_workflow():
    """Verify complete CRUD workflow."""
    # Create
    task = engine.create_task("Buy groceries", "Milk, bread, eggs")
    task_id = task["id"]

    # Read
    all_tasks = engine.get_all_tasks()
    assert len(all_tasks) == 1

    # Update
    success = engine.update_task(task_id, description="Milk, bread, butter")
    assert success is True

    # Toggle
    success = engine.toggle_task_status(task_id)
    assert success is True
    task = engine.get_task_by_id(task_id)
    assert task["status"] == "Completed"

    # Delete
    success = engine.delete_task(task_id)
    assert success is True
    assert engine.get_task_by_id(task_id) is None
    assert len(engine.get_all_tasks()) == 0


def test_multiple_tasks_workflow():
    """Verify workflow with multiple tasks."""
    # Create 3 tasks
    task1 = engine.create_task("Task 1", "")
    task2 = engine.create_task("Task 2", "")
    engine.create_task("Task 3", "")

    # Verify all exist
    assert len(engine.get_all_tasks()) == 3

    # Toggle and update
    engine.toggle_task_status(task1["id"])
    engine.update_task(task2["id"], title="Updated Task 2")

    # Delete one
    engine.delete_task(task2["id"])

    # Verify state
    tasks = engine.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0]["status"] == "Completed"
    assert tasks[1]["title"] == "Task 3"
