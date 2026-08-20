# Studymate Bot

## Project Specification

**Version:** 2.0 (MVP)

**Author:** Darya Pavlova

---

# 1. Project Overview

Studymate Bot is a Telegram bot designed to help students organize their academic workload.

The bot allows users to manage university subjects and tasks directly through Telegram using a button-based interface.

Users can create subjects, add tasks with descriptions, priorities and deadlines, mark tasks as completed, edit task information, review upcoming and overdue tasks, and view statistics about their workload.

The project was developed as a practical backend-oriented application and portfolio project demonstrating Python development, Telegram Bot API integration, database design, ORM usage, testing and documentation.

---

# 2. Goals

## Functional Goals

The bot allows users to:

- create and manage academic subjects;
- create and manage tasks;
- assign tasks to subjects;
- add optional task descriptions;
- set task priorities;
- set and change deadlines;
- mark tasks as completed;
- edit task information;
- view all current tasks;
- view upcoming tasks;
- view overdue tasks;
- view tasks without deadlines;
- view workload statistics;
- configure notification-related settings;
- permanently store application data.

## Learning Goals

The project was developed to improve practical skills in:

- Python project architecture;
- Git and GitHub workflow;
- Telegram Bot API;
- aiogram 3.x;
- Finite State Machine (FSM);
- SQLite;
- SQLAlchemy ORM;
- environment variables;
- database session management;
- automated testing with pytest;
- error handling;
- clean code practices;
- technical documentation.

---

# 3. Target Users

The main target users are:

- university students;
- school students;
- online course learners.

The primary use case is managing academic assignments and deadlines.

---

# 4. Scope

## Included in MVP

### Subjects

The user can:

- create a subject;
- view their subjects;
- delete a subject.

Before deleting a subject, the system checks whether the subject contains tasks.

A subject with existing tasks cannot be deleted. This prevents accidental loss of related task data.

---

## Tasks

The user can:

- create a task;
- assign a task to a subject;
- add an optional description;
- set a priority;
- set an optional deadline;
- view tasks;
- mark a task as completed;
- edit the task title;
- edit the task description;
- edit the task deadline;
- edit the task priority;
- view overdue tasks;
- view upcoming tasks;
- view tasks without deadlines;
- delete tasks where supported by the application flow.

### Task properties

Each task can contain:

- title;
- optional description;
- subject;
- priority;
- optional deadline;
- completion state.

The default task priority is **Medium**.

Supported priorities include:

- Low;
- Medium;
- High.

Completed tasks are excluded from incomplete-task views such as overdue and upcoming tasks.

---

## Statistics

The bot provides workload statistics including:

- total number of subjects;
- total number of tasks;
- completed tasks;
- remaining tasks;
- tasks with deadlines;
- tasks without deadlines;
- overdue tasks;
- completion rate;
- number of tasks by subject.

Statistics are calculated separately for each user.

---

## Notifications and Settings

The application contains a settings section with notification-related functionality.

Notification settings are stored per user.

---

## User Management

The system identifies users through their Telegram user ID and keeps user-specific data isolated.

Users can only access their own subjects and tasks.

---

## Database

The application:

- uses SQLite for persistent storage;
- uses SQLAlchemy ORM for database interaction;
- stores users, subjects and tasks;
- maintains relationships between users, subjects and tasks.

---

# 5. Future Features

The following features are outside the current MVP and may be implemented in future versions:

- task archiving;
- calendar integration;
- Google Calendar synchronization;
- deadline notifications and reminders;
- tags;
- task search;
- advanced filtering;
- multiple languages;
- PostgreSQL support;
- Docker deployment;
- CSV/PDF export;
- Telegram Mini App;
- web interface;
- mobile application;
- AI assistant features;
- multi-user collaboration;
- cloud deployment.

These features are intentionally excluded from the current MVP to keep the project focused and maintainable.

---

# 6. User Stories

## US-1

As a student,

I want to create subjects,

so that I can organize my academic tasks.

---

## US-2

As a student,

I want to view my subjects,

so that I can see how my academic workload is organized.

---

## US-3

As a student,

I want to create tasks and assign them to subjects,

so that I can keep my assignments organized.

---

## US-4

As a student,

I want to add descriptions, priorities and deadlines to tasks,

so that I can store all relevant information about an assignment.

---

## US-5

As a student,

I want to mark tasks as completed,

so that I can track my progress.

---

## US-6

As a student,

I want to edit task information,

so that I can keep my assignments up to date.

---

## US-7

As a student,

I want to see overdue tasks,

so that I know which assignments require immediate attention.

---

## US-8

As a student,

I want to see upcoming tasks,

so that I can plan my workload in advance.

---

## US-9

As a student,

I want to see tasks without deadlines,

so that I can distinguish them from scheduled assignments.

---

## US-10

As a student,

I want to see statistics about my tasks,

so that I can understand my workload and completion progress.

---

# 7. Functional Requirements

## User Management

### FR-1

The system shall identify users by their Telegram user ID.

### FR-2

User-specific data shall be isolated between different Telegram users.

---

## Subject Management

### FR-3

The user shall be able to create a subject.

### FR-4

The user shall be able to view their subjects.

### FR-5

The user shall be able to delete a subject.

### FR-6

The system shall prevent deletion of a subject if it contains tasks.

---

## Task Management

### FR-7

The user shall be able to create a task.

### FR-8

Each task shall belong to exactly one subject.

### FR-9

A task may contain an optional description.

### FR-10

A task shall have a priority.

### FR-11

A task may have an optional deadline.

### FR-12

The user shall be able to mark a task as completed.

### FR-13

The user shall be able to edit the task title.

### FR-14

The user shall be able to edit the task description.

### FR-15

The user shall be able to edit the task priority.

### FR-16

The user shall be able to edit the task deadline.

### FR-17

The system shall prevent users from modifying or accessing tasks belonging to another user.

### FR-18

The system shall prevent duplicate task titles within the same subject where required by the application logic.

---

## Task Queries

### FR-19

The user shall be able to view their tasks.

### FR-20

The system shall provide a list of incomplete overdue tasks.

### FR-21

The system shall provide a list of incomplete tasks with deadlines within the next seven days.

### FR-22

The system shall provide a list of incomplete tasks without deadlines.

### FR-23

Tasks belonging to other users shall not appear in any task query.

### FR-24

A task with a deadline equal to today's date shall not be considered overdue.

---

## Statistics

### FR-25

The system shall calculate the total number of subjects for a user.

### FR-26

The system shall calculate the total number of tasks for a user.

### FR-27

The system shall calculate completed and remaining tasks.

### FR-28

The system shall calculate tasks with and without deadlines.

### FR-29

The system shall calculate overdue tasks.

### FR-30

The system shall calculate the task completion rate.

### FR-31

The system shall calculate the number of tasks belonging to each subject.

---

# 8. User Interface

The bot uses Telegram as its primary interface.

Users interact mainly through buttons and step-by-step conversations rather than text commands.

## Main Menu

The main navigation includes sections for:

```text
📚 Subjects
📝 Tasks
📊 Statistics
⚙ Settings
```

The exact button labels may vary depending on the current UI implementation.

---

## Subjects Menu

The subjects section provides functionality for:

```text
➕ Add Subject
📄 Show Subjects
🗑 Delete Subject
```

---

## Tasks Menu

The tasks section provides functionality for:

```text
➕ Add Task
📋 Show Tasks
✅ Complete Task
✏️ Edit Task
🗑 Delete Task
```

Additional task views are available for:

- overdue tasks;
- upcoming tasks;
- tasks without deadlines.

---

# 9. Task Creation Flow

Task creation uses FSM (Finite State Machine) to guide the user through several steps.

A typical flow is:

```text
User presses:

➕ Add Task

↓

Bot:

Enter task title

↓

User:

Linear Algebra homework

↓

Bot:

Add description (optional)

↓

User:

Exercises 1-15

or

Skip

↓

Bot:

Choose subject

↓

User:

Linear Algebra

↓

Bot:

Choose priority

↓

User:

High

↓

Bot:

Enter deadline (optional)

↓

User:

15-09-2026

↓

Task is created.
```

The exact flow may vary depending on the selected options.

---

# 10. Task Management Flows

## Complete Task

```text
User selects:

✅ Complete Task

↓

Bot displays available tasks

↓

User selects a task

↓

Task is marked as completed.
```

---

## Edit Task

The user can select a task and modify supported properties, including:

- title;
- description;
- priority;
- deadline.

---

## Overdue Tasks

An incomplete task is considered overdue when:

```text
deadline < today
```

Tasks with today's deadline are not considered overdue.

---

## Upcoming Tasks

Upcoming tasks are incomplete tasks with a deadline from tomorrow through seven days from today.

Tasks beyond the seven-day period are not included.

---

# 11. Data Model

## User

Main fields:

```text
id
telegram_id
username
created_at
```

---

## Subject

Main fields:

```text
id
user_id
name
created_at
```

---

## Task

Main fields:

```text
id
subject_id
title
description
deadline
completed
priority
created_at
updated_at
```

---

# Relationships

```text
User
 |
 | one-to-many
 |
Subjects
 |
 | one-to-many
 |
Tasks
```

Each subject belongs to one user.

Each task belongs to one subject.

The subject relationship is used to enforce user-level data isolation.

---

# 12. Technologies

## Language

- Python 3.13

## Framework

- aiogram 3.x

## Database

- SQLite

## ORM

- SQLAlchemy

## Configuration

- python-dotenv

## Testing

- pytest

## Version Control

- Git
- GitHub

---

# 13. Project Structure

The project is organized into separate application, database, handler, keyboard and test modules.

A simplified structure is:

```text
Studymate-Bot/

├── src/
│   ├── main.py
│   ├── bot.py
│   ├── config.py
│   │
│   ├── handlers/
│   ├── keyboards/
│   │
│   └── database/
│       ├── db.py
│       ├── models.py
│       ├── subjects.py
│       ├── tasks.py
│       └── statistics.py
│
├── tests/
│   ├── test_subjects.py
│   ├── test_tasks.py
│   └── test_statistics.py
│
├── docs/
│   └── Project_Specification.md
│
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

The structure may evolve as the project grows.

---

# 14. Testing

The project uses pytest for automated testing.

Tests cover the main database operations and business logic, including:

- subject creation;
- subject lookup;
- subject deletion;
- subject ownership;
- task creation;
- duplicate task handling;
- task ownership;
- task completion;
- task editing;
- deadlines;
- overdue tasks;
- upcoming tasks;
- tasks without deadlines;
- task statistics;
- user isolation.

The tests use an isolated in-memory SQLite database.

The test suite is designed to verify both successful operations and invalid or unauthorized operations.

Tests can be executed with:

```bash
pytest
```

---

# 15. Development Roadmap

## Phase 1 — Project Setup

- create repository;
- configure virtual environment;
- install dependencies;
- create project structure;
- configure environment variables.

**Status: Completed**

---

## Phase 2 — Telegram Bot Foundation

- create bot;
- connect aiogram;
- implement `/start`;
- create main menu;
- configure button navigation.

**Status: Completed**

---

## Phase 3 — Subject Management

- create subject;
- display subjects;
- delete subjects;
- prevent deletion when tasks exist.

**Status: Completed**

---

## Phase 4 — Task Management

- create tasks;
- add descriptions;
- assign subjects;
- set priorities;
- set deadlines;
- complete tasks;
- edit tasks;
- delete tasks;
- view overdue tasks;
- view upcoming tasks;
- view tasks without deadlines.

**Status: Completed**

---

## Phase 5 — Database Integration

- create database models;
- configure SQLite;
- connect SQLAlchemy;
- implement persistent storage;
- isolate user data.

**Status: Completed**

---

## Phase 6 — Statistics and Settings

- implement task statistics;
- calculate completion rate;
- group tasks by subject;
- implement notification-related settings.

**Status: Completed**

---

## Phase 7 — Testing

- add automated tests;
- test normal operations;
- test invalid operations;
- test user isolation;
- test edge cases.

**Status: Completed**

---

## Phase 8 — Project Polishing

- improve README;
- update technical documentation;
- add screenshots;
- review `.env.example`;
- review `.gitignore`;
- review `requirements.txt`;
- clean repository;
- prepare portfolio presentation.

**Status: In Progress**

---

# 16. MVP Success Criteria

The MVP is considered complete when:

- the bot starts successfully;
- users can access only their own data;
- subjects can be created, viewed and deleted safely;
- subjects containing tasks cannot be deleted;
- tasks can be created and managed;
- tasks support descriptions;
- tasks support priorities;
- tasks support optional deadlines;
- tasks can be completed;
- task information can be edited;
- overdue tasks can be viewed;
- upcoming tasks can be viewed;
- tasks without deadlines can be viewed;
- statistics are available;
- data persists between application restarts;
- automated tests pass;
- project documentation is available;
- configuration examples are provided;
- generated/local database files are excluded from Git;
- the repository is ready for public GitHub publication.

---

# 17. Known Limitations

The current MVP intentionally does not provide:

- cloud synchronization;
- calendar integration;
- AI-powered task management;
- web or mobile interface;
- multi-user collaboration;
- advanced task search;
- task archiving;
- production deployment infrastructure.

The project is primarily intended as a functional portfolio project and learning application rather than a production-scale service.

---

# 18. Future Development

Possible future improvements include:

- deadline notifications;
- recurring tasks;
- task tags;
- search and filtering;
- calendar integration;
- Google Calendar synchronization;
- PostgreSQL;
- Docker;
- cloud deployment;
- CSV/PDF export;
- multilingual support;
- Telegram Mini App;
- web interface;
- AI assistant;
- advanced analytics.

---

# 19. Project Status

**Current status: MVP completed, portfolio polishing in progress.**

The core functionality, database layer, business logic and automated tests are implemented.

The remaining work is focused primarily on documentation, repository presentation, screenshots and final GitHub cleanup.
