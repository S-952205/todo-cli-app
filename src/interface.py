"""
CLI interface and user interaction functions.

Provides menu display, input prompts, and formatted output using the rich library.
"""

from rich.table import Table
from rich.console import Console

console = Console()


def show_message(message: str) -> None:
    """
    Display a neutral message to the user.

    Args:
        message: The message to display

    Example:
        >>> show_message("This is a message")
        This is a message
    """
    console.print(message)


def show_success(message: str) -> None:
    """
    Display a success message in green.

    Args:
        message: The success message to display

    Example:
        >>> show_success("Task created!")
        ✓ Task created!
    """
    console.print(f"[green]✓ {message}[/green]")


def show_error(message: str) -> None:
    """
    Display an error message in red.

    Args:
        message: The error message to display

    Example:
        >>> show_error("Invalid input")
        ✗ Invalid input
    """
    console.print(f"[red]✗ {message}[/red]")


def prompt_string(prompt_text: str, required: bool = False) -> str:
    """
    Prompt user for a string input.

    Args:
        prompt_text: The prompt message to display
        required: If True, reprompt if user enters empty string

    Returns:
        The user input (stripped of leading/trailing whitespace)

    Example:
        >>> user_input = prompt_string("Enter task title: ", required=True)
    """
    while True:
        user_input = console.input(f"[bold]{prompt_text}[/bold]").strip()
        if user_input or not required:
            return user_input
        show_error("Input cannot be empty. Please try again.")


def prompt_integer(prompt_text: str) -> int | None:
    """
    Prompt user for an integer input.

    Args:
        prompt_text: The prompt message to display

    Returns:
        The integer input, or None if user enters invalid input

    Example:
        >>> task_id = prompt_integer("Enter task ID: ")
        >>> if task_id is None:
        ...     show_error("Please enter a valid number")
    """
    try:
        user_input = console.input(f"[bold]{prompt_text}[/bold]").strip()
        if not user_input:
            show_error("Please enter a number.")
            return None
        return int(user_input)
    except ValueError:
        show_error(f"Please enter a valid number, not '{user_input}'.")
        return None


def display_menu() -> str:
    """
    Display the main menu and get user's choice.

    Returns:
        User's menu choice as a string (e.g., "1", "add", "exit")

    Note:
        Reprompts if user enters invalid choice.

    Example:
        >>> choice = display_menu()
        >>> # User sees menu and enters "1"
        >>> choice
        '1'
    """
    console.print("\n[bold cyan]Main Menu[/bold cyan]:")
    console.print("  1. Add Task")
    console.print("  2. View Tasks")
    console.print("  3. Update Task")
    console.print("  4. Delete Task")
    console.print("  5. Toggle Task Status")
    console.print("  6. Exit")

    while True:
        choice = console.input("\n[bold]Enter your choice (1-6):[/bold] ").strip().lower()

        # Accept numeric or word input
        if choice in ("1", "add"):
            return "1"
        elif choice in ("2", "view"):
            return "2"
        elif choice in ("3", "update"):
            return "3"
        elif choice in ("4", "delete"):
            return "4"
        elif choice in ("5", "toggle"):
            return "5"
        elif choice in ("6", "exit"):
            return "6"
        else:
            show_error("Invalid choice. Please enter 1-6 or a valid operation name.")


def prompt_task_creation() -> tuple:
    """
    Prompt user to create a new task with title and description.

    Returns:
        Tuple of (title, description) strings

    Example:
        >>> title, desc = prompt_task_creation()
        >>> title
        'Buy milk'
        >>> desc
        'From the store'
    """
    title = prompt_string("Enter task title: ", required=True)
    description = prompt_string("Enter task description (optional): ", required=False)
    return (title, description)


def prompt_task_id() -> int | None:
    """
    Prompt user to enter a task ID.

    Returns:
        The task ID as an integer, or None if invalid input

    Example:
        >>> task_id = prompt_task_id()
    """
    return prompt_integer("Enter task ID: ")


def prompt_update_fields() -> tuple:
    """
    Prompt user to enter new title and/or description for update.

    Returns:
        Tuple of (title, description) where each is a string or None
        None means "don't change this field"

    Example:
        >>> title, desc = prompt_update_fields()
        >>> # If user skips title: title is None
        >>> # If user enters new title: title is the new string
    """
    console.print("[yellow]Leave blank to keep the current value[/yellow]")

    # Prompt for title (optional for update)
    title_input = console.input("[bold]Enter new title (or press Enter to skip):[/bold] ").strip()
    title = title_input if title_input else None

    # Prompt for description (optional for update)
    desc_input = console.input(
        "[bold]Enter new description (or press Enter to skip):[/bold] "
    ).strip()
    description = desc_input if desc_input else None

    return (title, description)


def display_tasks(tasks: list) -> None:
    """
    Display all tasks in a formatted table using rich.

    Args:
        tasks: List of task dicts to display

    Note:
        If no tasks, displays a message instead.

    Example:
        >>> tasks = [
        ...     {'id': 1, 'title': 'Buy milk', 'description': 'From store', 'status': 'Pending'},
        ...     {'id': 2, 'title': 'Exercise', 'description': '', 'status': 'Completed'}
        ... ]
        >>> display_tasks(tasks)
    """
    if not tasks:
        show_message("[yellow]No tasks exist. Create one to get started![/yellow]")
        return

    # Create table
    table = Table(title="Your Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Status", style="yellow")

    # Add rows
    for task in tasks:
        status_display = (
            "[green][X] Completed[/green]"
            if task["status"] == "Completed"
            else "[white][ ] Pending[/white]"
        )
        table.add_row(
            str(task["id"]),
            task["title"],
            task["description"] if task["description"] else "(empty)",
            status_display,
        )

    # Print table
    console.print(table)
