---
name: cli-ui-designer
description: Standards for terminal-based user interfaces, menus, and table formatting.
---

# CLI Interface Skill

This skill provides instructions for creating a clean and user-friendly terminal experience.

## UI Standards
- **Icons**: Use `[ ]` for Pending and `[X
]` for Completed tasks.
- **Menu**: Use a numeric menu (1-6) for navigation.
- **Feedback**: 
  - Show a green success message after every action: `Successfully [Action] task #[ID]`.
  - Show error messages in a clear format: `Error: [Message]`.

## Layout Requirements
- **Table Headers**: ID | Status | Title | Description.
- **Spacing**: Ensure columns are aligned using string padding (e.g., `.ljust()`).
- **Clearing**: Clear the terminal screen before redisplaying the menu to keep it tidy.