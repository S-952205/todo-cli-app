"""
Task entity model and validation functions.

Defines the Task data structure and validation rules for task attributes.
"""


def validate_title(title: str) -> bool:
    """
    Validate that a task title is non-empty and non-whitespace.

    Args:
        title: The task title to validate

    Returns:
        True if valid

    Raises:
        ValueError: If title is empty or contains only whitespace
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    return True


def validate_description(description: str) -> str:
    """
    Validate and normalize a task description.

    Args:
        description: The task description to validate

    Returns:
        The stripped description (leading/trailing whitespace removed)

    Note:
        Description can be empty; only whitespace is stripped.
    """
    return description.strip() if description else ""


def validate_status(status: str) -> bool:
    """
    Validate that a task status is one of the allowed values.

    Args:
        status: The task status to validate

    Returns:
        True if valid

    Raises:
        ValueError: If status is not "Pending" or "Completed"
    """
    if status not in ("Pending", "Completed"):
        raise ValueError('Status must be "Pending" or "Completed"')
    return True


# Task type definition (using dict for simplicity)
# Task = {
#     "id": int,              # Unique identifier (auto-assigned, sequential)
#     "title": str,           # Non-empty task title
#     "description": str,     # Task details (can be empty)
#     "status": str           # "Pending" or "Completed"
# }
