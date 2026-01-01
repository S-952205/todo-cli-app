---
name: todo-logic-expert
description: Guidelines for managing CRUD operations, unique ID generation, and in-memory data integrity.
---

# Todo Logic Skill

This skill ensures that the core application logic remains robust and follows consistent patterns.

## Core Rules
- **Unique IDs**: Always use an auto-incrementing integer starting from 1. Never reuse an ID after deletion in a single session.
- **Data Structure**: Store tasks as a list of dictionaries: `{"id": int, "title": str, "desc": str, "status": bool}`.
- **Validation**:
  - Title cannot be empty or just whitespace.
  - IDs must be verified for existence before Update or Delete operations.

## Procedures
- **Add**: Initialize `status` as `False` (Pending).
- **Toggle**: Switch `status` between `True` and `False`.
- **Search**: Use list comprehension for fast ID-based lookups.