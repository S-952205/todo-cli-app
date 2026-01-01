"""
Integration tests for complete workflows.

Tests end-to-end user scenarios combining engine and interface.
"""

import pytest
from src import engine


@pytest.fixture(autouse=True)
def reset_engine():
    """Reset engine state before each test."""
    engine._reset_state()
    yield
    engine._reset_state()


def test_add_view_complete_workflow():
    """Test: Add task → View task list → Verify display."""
    # Add multiple tasks
    engine.create_task("Buy milk", "From the store")
    engine.create_task("Exercise", "30 minutes")
    engine.create_task("Read book", "")

    # Verify all tasks exist
    all_tasks = engine.get_all_tasks()
    assert len(all_tasks) == 3

    # Verify task details
    assert all_tasks[0]["title"] == "Buy milk"
    assert all_tasks[0]["status"] == "Pending"
    assert all_tasks[1]["title"] == "Exercise"
    assert all_tasks[2]["title"] == "Read book"
    assert all_tasks[2]["description"] == ""


def test_add_update_view_workflow():
    """Test: Add task → Update → View changes."""
    # Add task
    task = engine.create_task("Original Title", "Original Description")
    task_id = task["id"]

    # Update
    engine.update_task(task_id, title="Updated Title")
    engine.update_task(task_id, description="Updated Description")

    # Verify update
    updated_task = engine.get_task_by_id(task_id)
    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == "Updated Description"
    assert updated_task["status"] == "Pending"


def test_add_toggle_view_workflow():
    """Test: Add task → Toggle status → View status change."""
    # Add task (starts as Pending)
    task = engine.create_task("Task to complete", "")
    task_id = task["id"]

    assert engine.get_task_by_id(task_id)["status"] == "Pending"

    # Toggle to Completed
    engine.toggle_task_status(task_id)
    assert engine.get_task_by_id(task_id)["status"] == "Completed"

    # Toggle back to Pending
    engine.toggle_task_status(task_id)
    assert engine.get_task_by_id(task_id)["status"] == "Pending"


def test_add_delete_view_workflow():
    """Test: Add tasks → Delete one → Verify removal."""
    # Add tasks
    task1 = engine.create_task("Task 1", "")
    task2 = engine.create_task("Task 2", "")
    task3 = engine.create_task("Task 3", "")

    # Verify all exist
    assert len(engine.get_all_tasks()) == 3

    # Delete task 2
    engine.delete_task(task2["id"])

    # Verify deletion
    all_tasks = engine.get_all_tasks()
    assert len(all_tasks) == 2
    assert engine.get_task_by_id(task2["id"]) is None
    assert engine.get_task_by_id(task1["id"]) is not None
    assert engine.get_task_by_id(task3["id"]) is not None


def test_error_handling_invalid_title():
    """Test error handling: Reject empty titles."""
    with pytest.raises(ValueError):
        engine.create_task("", "")

    with pytest.raises(ValueError):
        engine.create_task("   ", "")

    # Verify no tasks were created
    assert len(engine.get_all_tasks()) == 0


def test_error_handling_invalid_id_operations():
    """Test error handling: Operations on non-existent IDs."""
    # Create a task first
    engine.create_task("Task", "")

    # Try operations on non-existent ID
    assert engine.get_task_by_id(999) is None
    assert engine.update_task(999, title="New") is False
    assert engine.delete_task(999) is False
    assert engine.toggle_task_status(999) is False


def test_boundary_condition_many_tasks():
    """Test system behavior with many tasks."""
    # Create 50 tasks
    for i in range(50):
        engine.create_task(f"Task {i+1}", f"Description {i+1}")

    # Verify all exist
    all_tasks = engine.get_all_tasks()
    assert len(all_tasks) == 50

    # Verify IDs are sequential
    for i, task in enumerate(all_tasks):
        assert task["id"] == i + 1

    # Delete every other task
    for i in range(1, 51, 2):
        engine.delete_task(i)

    # Verify 25 tasks remain
    remaining_tasks = engine.get_all_tasks()
    assert len(remaining_tasks) == 25


def test_boundary_condition_empty_description():
    """Test system behavior with empty descriptions."""
    task = engine.create_task("Task without description", "")

    assert task["description"] == ""

    # Update with empty description
    engine.update_task(task["id"], description="")
    updated = engine.get_task_by_id(task["id"])
    assert updated["description"] == ""


def test_boundary_condition_long_text():
    """Test system behavior with very long titles and descriptions."""
    long_title = "A" * 1000
    long_desc = "B" * 1000

    task = engine.create_task(long_title, long_desc)

    assert task["title"] == long_title
    assert task["description"] == long_desc

    # Retrieve and verify
    retrieved = engine.get_task_by_id(task["id"])
    assert len(retrieved["title"]) == 1000
    assert len(retrieved["description"]) == 1000


def test_id_counter_persistence():
    """Test that ID counter persists correctly across operations."""
    task1 = engine.create_task("Task 1", "")
    assert task1["id"] == 1

    task2 = engine.create_task("Task 2", "")
    assert task2["id"] == 2

    # Delete task 1
    engine.delete_task(1)

    # Next task should still get ID 3
    task3 = engine.create_task("Task 3", "")
    assert task3["id"] == 3

    # Verify IDs
    all_tasks = engine.get_all_tasks()
    ids = [t["id"] for t in all_tasks]
    assert ids == [2, 3]


def test_status_transitions():
    """Test status transitions: Pending → Completed → Pending."""
    task = engine.create_task("Task", "")

    # Initial state
    assert engine.get_task_by_id(task["id"])["status"] == "Pending"

    # Toggle to Completed
    engine.toggle_task_status(task["id"])
    assert engine.get_task_by_id(task["id"])["status"] == "Completed"

    # Toggle back to Pending
    engine.toggle_task_status(task["id"])
    assert engine.get_task_by_id(task["id"])["status"] == "Pending"

    # Toggle multiple times
    for _ in range(5):
        engine.toggle_task_status(task["id"])

    # Should be Completed after odd number of toggles
    assert engine.get_task_by_id(task["id"])["status"] == "Completed"
