"""
Main application entry point and event loop.

Orchestrates the interaction between the CLI interface and business logic engine.
"""

from src import interface, engine


def main() -> None:
    """
    Run the Todo CLI application.

    This is the main event loop that:
    1. Displays the menu and gets user choice
    2. Routes to appropriate operation handler
    3. Repeats until user chooses to exit

    Example:
        >>> main()
        # App runs and accepts user commands
    """
    # Welcome message
    interface.show_message("\n[bold cyan]╔═════════════════════════════════════╗[/bold cyan]")
    interface.show_message("[bold cyan]║     Welcome to Todo App Phase 1     ║[/bold cyan]")
    interface.show_message("[bold cyan]╚═════════════════════════════════════╝[/bold cyan]\n")

    # Main event loop
    while True:
        choice = interface.display_menu()

        # Handle Add Task (choice "1")
        if choice == "1":
            try:
                title, description = interface.prompt_task_creation()
                task = engine.create_task(title, description)
                interface.show_success(f"Task created with ID {task['id']}: {title}")
            except ValueError as e:
                interface.show_error(str(e))

        # Handle View Tasks (choice "2")
        elif choice == "2":
            tasks = engine.get_all_tasks()
            interface.display_tasks(tasks)

        # Handle Update Task (choice "3")
        elif choice == "3":
            task_id = interface.prompt_task_id()
            if task_id is None:
                continue

            # Get current task to show user what they're editing
            task = engine.get_task_by_id(task_id)
            if task is None:
                interface.show_error(f"Task with ID {task_id} not found.")
                continue

            # Show current task info
            interface.show_message(
                f"\n[cyan]Current task: '{task['title']}' - {task['description']}"
            )

            # Get new values
            title, description = interface.prompt_update_fields()

            # Perform update
            try:
                success = engine.update_task(task_id, title, description)
                if success:
                    interface.show_success(f"Task {task_id} updated successfully.")
                else:
                    interface.show_error(f"Task with ID {task_id} not found.")
            except ValueError as e:
                interface.show_error(str(e))

        # Handle Delete Task (choice "4")
        elif choice == "4":
            task_id = interface.prompt_task_id()
            if task_id is None:
                continue

            success = engine.delete_task(task_id)
            if success:
                interface.show_success(f"Task {task_id} deleted successfully.")
            else:
                interface.show_error(f"Task with ID {task_id} not found.")

        # Handle Toggle Task Status (choice "5")
        elif choice == "5":
            task_id = interface.prompt_task_id()
            if task_id is None:
                continue

            success = engine.toggle_task_status(task_id)
            if success:
                task = engine.get_task_by_id(task_id)
                interface.show_success(f"Task {task_id} status changed to {task['status']}.")
            else:
                interface.show_error(f"Task with ID {task_id} not found.")

        # Handle Exit (choice "6")
        elif choice == "6":
            interface.show_message(
                "[bold cyan]Thank you for using Todo App! Goodbye![/bold cyan]\n"
            )
            break


if __name__ == "__main__":
    main()
