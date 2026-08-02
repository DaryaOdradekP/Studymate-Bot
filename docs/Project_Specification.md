# Studymate Bot

## Project Specification

**Version:** 1.0 (MVP)

**Author:** Darya Pavlova

---

# 1. Project Overview

Studymate Bot is a Telegram bot designed to help students organize their academic life.

The bot allows users to manage university subjects, assignments and deadlines directly through Telegram using an intuitive button-based interface.

The main purpose of the project is to create a practical productivity tool while demonstrating backend development skills using Python.

---

# 2. Goals

## Functional Goals

The bot should allow users to:

- manage academic subjects;
- create and organize assignments;
- track deadlines;
- mark assignments as completed;
- archive unnecessary tasks;
- quickly view current workload;
- permanently store user data.

---

## Learning Goals

During the development of this project, I want to improve my skills in:

- Python project architecture;
- Git and GitHub workflow;
- Telegram Bot API;
- aiogram framework;
- Finite State Machine (FSM);
- SQLite database;
- SQLAlchemy ORM;
- environment variables;
- clean code practices;
- software documentation.

---

# 3. Target Users

The main users of the application are:

- university students;
- school students;
- online course learners.

---

# 4. Scope

## Included in MVP

## Subjects

The user can:

- create a subject;
- view all subjects;
- archive/delete a subject.

Before deleting a subject, the system should check whether it contains active tasks.

---

## Tasks

The user can:

- create a task;
- add an optional description;
- select a related subject;
- set a deadline;
- view active tasks;
- mark tasks as completed;
- archive tasks.

Task statuses:

```
Active
Completed
Archived
```

---

## User

The system should:

- automatically register a user on the first launch;
- store basic Telegram user information.

---

## Database

The system should:

- store data permanently;
- use SQLite as the database;
- use SQLAlchemy for database interaction.

---

# Not Included in MVP

The following features are planned for future versions:

- Google Calendar integration;
- cloud database;
- AI assistant features;
- PDF export;
- web interface;
- mobile application;
- multi-user collaboration.

---

# 5. User Stories

## US-1

As a student,

I want to create subjects,

so that I can organize my assignments.

---

## US-2

As a student,

I want to add assignments with optional descriptions,

so that I can keep additional information about my tasks.

---

## US-3

As a student,

I want to see my active assignments,

so that I know what needs to be completed.

---

## US-4

As a student,

I want to mark assignments as completed,

so that I can track my progress.

---

## US-5

As a student,

I want to archive unnecessary assignments,

so that I can keep my task list clean without permanently deleting information.

---

## US-6

As a student,

I want to see today's tasks,

so that I can focus on my current workload.

---

# 6. Functional Requirements

## User Management

### FR-1

The system shall automatically register a new user after the first interaction with the bot.

---

### FR-2

The system shall store:

- Telegram ID;
- username;
- registration date.

---

# Subject Management

### FR-3

The user shall be able to create subjects.

---

### FR-4

The user shall be able to view their subjects.

---

### FR-5

The user shall be able to remove subjects.

If a subject contains tasks, the system should request confirmation before deletion.

---

# Task Management

### FR-6

The user shall be able to create tasks.

---

### FR-7

Each task shall contain:

- title;
- optional description;
- deadline;
- status;
- creation date.

---

### FR-8

Each task shall belong to exactly one subject.

---

### FR-9

The user shall be able to change task status:

```
Active → Completed

Active → Archived
```

---

### FR-10

The user shall be able to view:

- active tasks;
- completed tasks;
- archived tasks.

---

# 7. User Interface

The bot uses Telegram as the main interface.

The user interacts mainly through buttons instead of text commands.

---

# Main Menu

```
📚 Subjects

📝 Tasks

📅 Today

📊 Statistics

⚙ Settings
```

---

# Subjects Menu

```
➕ Add Subject

📄 Show Subjects

🗑 Delete Subject
```

---

# Tasks Menu

```
➕ Add Task

📋 Show Tasks

✅ Complete Task

🗂 Archive Task

♻ Archived Tasks
```

---

# 8. Task Creation Flow

The bot uses a step-by-step dialogue based on FSM (Finite State Machine).

Example:

```
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

Enter deadline

↓

User:

15-10-2026

↓

Task is created.
```

---

# 9. Data Model

## User

Fields:

```
id
telegram_id
username
created_at
```

---

## Subject

Fields:

```
id
user_id
name
created_at
```

---

## Task

Fields:

```
id
subject_id
title
description (optional)
deadline
status
created_at
updated_at
```

---

# Relationships

```
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

---

# 10. Technologies

## Language

- Python 3.13

## Framework

- aiogram 3.x

## Database

- SQLite

## ORM

- SQLAlchemy

## Libraries

- python-dotenv

## Version Control

- Git
- GitHub

## Testing

- pytest (planned)

---

# 11. Project Structure

```
Studymate-Bot/

src/

├── main.py
├── bot.py
├── config.py

├── handlers/

├── keyboards/

├── database/

├── models/

├── services/

└── utils/


docs/

└── Project_Specification.md


tests/


README.md

requirements.txt

.env.example

.gitignore
```

---

# 12. Development Roadmap

# Phase 1 — Project Setup

Tasks:

- create repository;
- configure virtual environment;
- install dependencies;
- create project structure;
- configure environment variables.

---

# Phase 2 — Telegram Bot Foundation

Tasks:

- create bot using BotFather;
- connect aiogram;
- implement `/start`;
- create main menu;
- configure button navigation.

---

# Phase 3 — Subject Management

Tasks:

- create subject;
- display subjects;
- delete subjects;
- add confirmation logic.

---

# Phase 4 — Task Management

Tasks:

- create tasks;
- add optional description;
- select subject;
- set deadline;
- complete tasks;
- archive tasks.

---

# Phase 5 — Database Integration

Tasks:

- create database models;
- configure SQLite;
- connect SQLAlchemy;
- save and retrieve data.

---

# Phase 6 — Improvements

Tasks:

- improve user interface;
- add statistics;
- add error handling;
- improve code structure.

---

# Phase 7 — Project Polishing

Tasks:

- improve README;
- add screenshots;
- refactor code;
- prepare final GitHub repository.

---

# 13. MVP Success Criteria

The MVP is considered complete when:

- the bot starts successfully;
- users are automatically registered;
- subjects can be created and managed;
- tasks can be created and managed;
- tasks support descriptions and deadlines;
- tasks can be completed or archived;
- data remains after restarting the bot;
- the project contains documentation;
- the repository is publicly available on GitHub.

---

# 14. Version 2 Ideas

Possible future improvements:

- deadline notifications;
- task priorities;
- tags;
- search;
- calendar view;
- statistics by subject;
- multiple languages;
- Docker;
- PostgreSQL;
- export to CSV/PDF;
- Telegram Mini App interface.
